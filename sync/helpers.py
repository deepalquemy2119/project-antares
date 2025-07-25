from app.ddbb.connection.conector import get_mysql_connection

def enqueue_sync(table_name: str, record_id: int, action: str):
    """
    Inserta un evento en la tabla sync_queue para que Celery lo procese y sincronice con Firebase.

    :param table_name: Nombre de la tabla (ej: 'users', 'courses', etc.)
    :param record_id: ID del registro afectado
    :param action: 'INSERT', 'UPDATE' o 'DELETE'
    """
    valid_actions = ('INSERT', 'UPDATE', 'DELETE')
    if action not in valid_actions:
        raise ValueError(f"[enqueue_sync] Acción inválida: {action}. Debe ser una de {valid_actions}")

    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO sync_queue (table_name, record_id, action, processed, created_at)
            VALUES (%s, %s, %s, %s, NOW())
            """,
            (table_name, record_id, action, False)
        )
        conn.commit()
        print(f"[DEBUG] Evento en cola -> tabla={table_name} id={record_id} action={action}")
    finally:
        cursor.close()
        conn.close()
