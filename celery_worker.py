
import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)  # para que pueda encontrar carpetas en el nivel de celery_worker.py


from celery import Celery
from flask import Flask
from sync.sync_utils import sync_mysql_to_firebase
from ddbb.connection.conector import get_mysql_connection
import time


# Ajustar path para importar correctamente módulos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, 'sync'))
sys.path.append(os.path.join(BASE_DIR, 'firebase'))
sys.path.append(os.path.join(BASE_DIR, 'app'))

# Configuración Flask y Celery
app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
TaskBase = celery.Task

class ContextTask(TaskBase):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

celery.Task = ContextTask


@celery.task(name="sync.mysql_to_firebase")
def task_mysql_to_firebase():
    print("[Celery] Ejecutando sync MySQL → Firebase...")
    sync_mysql_to_firebase()
    print("[Celery] Listo!")


@celery.task(name="sync.firebase_to_mysql")
def task_firebase_to_mysql():
    print("[Celery] Ejecutando sync Firebase → MySQL...")
    sync_firebase_to_mysql()
    print("[Celery] Listo!")


@celery.task(name="sync.listen_sync_queue")
def listen_sync_queue():
    print("[Sync] Escuchando tabla sync_queue...")
    while True:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sync_queue WHERE processed = FALSE LIMIT 5")
        rows = cursor.fetchall()

        for row in rows:
            print(f"[Sync] Procesando acción: {row['action']} en tabla {row['table_name']} (ID {row['record_id']})")
            # Lógica para sincronizar según tabla afectada:
            if row['table_name'] == 'materials':
                sync_mysql_to_firebase()
            elif row['table_name'] == 'other_table':
                # Aquí otra sincronización si fuera necesaria
                pass
            # Marcar el registro como procesado
            cursor.execute("UPDATE sync_queue SET processed = TRUE WHERE id = %s", (row['id'],))

        conn.commit()
        cursor.close()
        conn.close()
        time.sleep(10)  # Esperar 10 segundos antes de volver a consultar
