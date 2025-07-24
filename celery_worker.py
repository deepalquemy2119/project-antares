from celery import Celery
import sys
import os
from flask import Flask

from sync.process_sync_queue import process_sync_queue
# función de sincronización

# el worker lee el script de sync
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'sync')))



# agrego carpeta `sync` al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'sync'))


def make_celery(app=None):
    app = app or Flask(__name__)
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    )


celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task


# # Config de Celery
# celery = Celery(__name__, backend='redis://localhost:6379/0', broker='redis://localhost:6379/0'
# )



    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
celery = make_celery(app)




# registramos la tarea
@celery.task(name="sync.process_queue")
def run_sync():
    print("[Celery] Ejecutando sincronización incremental...")
    process_sync_queue()
    print("[Celery] ✅ Sincronización completada")
