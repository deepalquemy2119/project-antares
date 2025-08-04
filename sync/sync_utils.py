# sync/sync_utils.py

import sys, os, time

# Agregar rutas necesarias
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'firebase')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from firebase.firebase_init import get_firebase_db
from app.utils.logger import get_logger
from app.ddbb.connection.conector import get_mysql_connection

logger = get_logger(__name__) if 'get_logger' in globals() else None

def upload_to_firebase(path, data):
    db_ref = get_firebase_db().reference(path)
    db_ref.set(data)

def delete_from_firebase(path):
    db_ref = get_firebase_db().reference(path)
    db_ref.delete()

def sync_mysql_to_firebase():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sync_queue WHERE processed = 0 ORDER BY created_at ASC")
    filas = cursor.fetchall()

    for fila in filas:
        tabla = fila['table_name']
        record_id = fila['record_id']
        accion = fila['action']
        sync_id = fila['id']

        logmsg = f"{accion} en {tabla}, id {record_id}"
        print(f"➡️ {logmsg}")
        if logger:
            logger.info(logmsg)

        try:
            if accion in ('INSERT', 'UPDATE'):
                cursor.execute(f"SELECT * FROM {tabla} WHERE id = %s", (record_id,))
                datos = cursor.fetchone()
                if datos:
                    for k, v in datos.items():
                        if isinstance(v, (bytes, bytearray)):
                            datos[k] = v.decode('utf-8', errors='ignore')
                    upload_to_firebase(f"{tabla}/{record_id}", datos)
                    print(f"✅ Sincronizado {tabla}/{record_id}")
                else:
                    delete_from_firebase(f"{tabla}/{record_id}")
                    print(f"⚠️ Registro no encontrado, eliminado {tabla}/{record_id}")
            elif accion == 'DELETE':
                delete_from_firebase(f"{tabla}/{record_id}")
                print(f"🗑️ Eliminado {tabla}/{record_id}")

            cursor.execute("UPDATE sync_queue SET processed = 1 WHERE id = %s", (sync_id,))
            conn.commit()

        except Exception as e:
            errmsg = f"Error procesando {tabla}/{record_id}: {e}"
            print(errmsg)
            if logger:
                logger.error(errmsg)

    cursor.close()
    conn.close()

def main():
    print("🔄 Iniciando sincronizador MySQL → Firebase… (Ctrl+C para detener)")
    while True:
        sync_mysql_to_firebase()
        time.sleep(2)

if __name__ == "__main__":
    main()
