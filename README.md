# project-antares

Estructura del proyecto:

Desde Manjaro: 

Para ver desde consola: tree -L 2 (con entorno activado)
(venv) jaden9112% tree -L 2

.
├── api
│   └── index.py
├── app
│   ├── ddbb
│   ├── decorators.py
│   ├── extensions.py
│   ├── __init__.py
│   ├── models.py
│   ├── __pycache__
│   ├── routes
│   ├── services
│   ├── static
│   ├── templates
│   └── utils
├── celery_worker.py
├── config.py
├── Dockerfile.test
├── dump.rdb
├── firebase
│   ├── firebase_init.py
│   ├── firebase-key.json
│   ├── __init__.py
│   └── __pycache__
├── LICENSE
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── __pycache__
│   ├── README
│   ├── script.py.mako
│   └── versions
├── __pycache__
│   ├── celery_worker.cpython-313.pyc
│   ├── config.cpython-311.pyc
│   └── config.cpython-313.pyc
├── pytest.ini
├── README.md
├── requirements.txt
├── run.py
├── seed_and_sync.py
├── sync
│   ├── helpers.py
│   ├── __init__.py
│   ├── process_sync_queue.py
│   ├── __pycache__
│   ├── sync_mysql_to_firebase.py
│   └── tasks.py
├── tests
│   ├── conftest.py
│   ├── __init__.py
│   ├── test_firebase.py
│   ├── test_login.py
│   ├── test_mysql.py
│   └── test_register.py
├── uploads
│   ├── course_1
│   ├── course_12
│   ├── course_3
│   ├── course_5
│   ├── course_6
│   └── course_7
└── venv
    ├── bin
    ├── include
    ├── lib
    ├── lib64 -> lib
    └── pyvenv.cfg

31 directories, 37 files

#===================================================
PARA INSTALAR DEPENDENCIAS Y LIBRERIAS: desde consola

Para instalar todo: $ pip install -r requirements.txt

#===================================================
PARA ENTRAR A LA BASE DE DATOS: ( no hay problemas, se puede probar, romper, cambiar,etc. Tengo un respaldo en otra cuenta )

Para ingresar a la DDBB de mysql: 
    desde consola o algun DBMS( yo use DBeaver ): 
        $ sudo mysql -u root -p: ---> contraseña del sistema ( windows, linux, o mac )
        $ Enter password: JadenKugo2119$&? ( contraseña para ingresar a la DDBB: ddbb_antares_project )

Seleccionar DDBB: $ use ddbb_antares_project; ( y estamos dentro de la base de datos )



#===================================================
para entrar a DDBB de FIREBASE: es usada como cache

# MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=JadenKugo2119$&?
DB_NAME=ddbb_antares_project

# Firebase
FIREBASE_CRED_PATH=/home/jaden9112/Escritorio/pro-ant/firebase/clave_privada.json
FIREBASE_DB_URL=https://antares-academy-default-rtdb.firebaseio.com/


FIREBASE_BUCKET_URL=gs://antares-academy.firebasestorage.app

# firebase-key.json:  (de firebase ) :


#===================================================
En el proyecto hay 3 tipos de usuarios: Alumnos, Tutores, y Admins

Los tutores solo pueden: 
            Crear cursos, subir materiales, eliminar materiales( editar ), o actualizar los cursos. CRUD.
            Pueden ver reseñas, y acciones que todavia NO he desarrollado( por tiempo ).


Los admins pueden casi de todo: 
            Me falta crear los protocolos de Regulacion de conducta en la plataforma para todos los tipos de usuarios.
            Son las reglas legales que regula el accionar de admin, tutores y alumnos por igual.

Los alumnos pueden:
            Inscribirse a cursos aprobados( los aprueban los admins, luego de que el tutor confirma que los materiales
             del curso, estan completos, y subidos a la plataforma ), pagar cuotas y recibir certificados, hacer reseñas
              de cursos, de tutores, y de otros compañeros.



#===================================================
Ejecutamos en consola. $ python run.py

para mysql: $ sudo mysql -u root -p  , luego password de mysql: JadenKugo2119$&?



#===================================================
celery_worker.py: 

import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)  # para que pueda encontrar carpetas en el nivel de celery_worker.py


from celery import Celery
from flask import Flask
from sync.sync_utils import sync_mysql_to_firebase
from app.ddbb.connection.conector import get_mysql_connection
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



#===================================================
.env:

# App Flask
SECRET_KEY=firebase-key.json

# MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=JadenKugo2119$&?
DB_NAME=ddbb_antares_project

# Firebase
FIREBASE_DB_URL=https://antares-academy-default-rtdb.firebaseio.com/
FIREBASE_CRED_PATH=./firebase/firebase-key.json


#FIREBASE_BUCKET_URL=gs://antares-academy.firebasestorage.app


# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Mail
GMAIL_USER=deepalquemy2119@gmail.com
GMAIL_APP_PASS=twdl ycmp xgfi gyih 
MAIL_DEFAULT_SENDER=deepalquemy2119@gmail.com



#===================================================







#===============================================================

