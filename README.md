# project-antares

Estructura del proyecto:
Para ver : (tree -L 2 (con entorno activado)
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
PARA INSTALAR DEPENDENCIAS Y LIBRERIAS:

Para instalar todo: pip install -r requirements.txt

#===================================================
PARA ENTRAR A LA BASE DE DATOS:

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











#===============================================================
Connect to MySQL and railway:
Private NetworkPublic Network
Connecting over the public network causes Egress costs.

Connection URL:


mysql://root:mVyzUfezAmAdiTvpuJQOZlbNgnIZeNcG@nozomi.proxy.rlwy.net:19064/railway


Raw

mysql

command: mysql -h nozomi.proxy.rlwy.net -u root -p

Pass:  mVyzUfezAmAdiTvpuJQOZlbNgnIZeNcG 
--port 19064 --protocol=TCP railway


Railway CLI connect command:

railway connect MySQL



Assign it the following value:

${{ MySQL.MYSQL_URL }}

