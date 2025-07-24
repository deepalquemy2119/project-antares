from celery_worker import celery
from conector import get_mysql_connection
from firebase_init import get_firebase_db

@celery.task
def process_sync_queue():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM sync_queue WHERE processed = FALSE ORDER BY created_at LIMIT 10")
        tasks = cursor.fetchall()

        for task in tasks:
            table = task['table_name']
            record_id = task['record_id']
            action = task['action']
            sync_id = task['id']

            firebase_path = f"{table}/{record_id}"

            if action in ('INSERT', 'UPDATE'):
                cursor.execute(f"SELECT * FROM {table} WHERE id = %s", (record_id,))
                record = cursor.fetchone()
                if record:
                    db_ref = get_firebase_db().reference(firebase_path)
                    db_ref.set(record)
                else:
                    print(f"Registro no encontrado: {table} id={record_id}")

            elif action == 'DELETE':
                db_ref = get_firebase_db().reference(firebase_path)
                db_ref.delete()

            cursor.execute("UPDATE sync_queue SET processed = TRUE WHERE id = %s", (sync_id,))
            conn.commit()

    finally:
        cursor.close()
        conn.close()
