# project-antares

Estructura del proyecto:

├── app/
│   ├── __init__.py        # crea la app, registra blueprints
│   ├── extensions.py      # db, login_manager, migrate
│   ├── models.py          # modelos SQLAlchemy
│   ├── templates/         # tus templates
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── ...
│   ├── static/            # css, js, imágenes
│   │   ├── css/
│   │   └── img/
│   ├── routes/            # vistas organizadas por módulo
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── admin_routes.py
│   │   ├── tutor_routes.py
│   │   ├── course_routes.py
│   │   └── public_routes.py
│   ├── ddbb/
│   │   └── connection/
│   │       └── conector.py
│   └── firebase/
│       └── firebase_init.py
│
├── migrations/            # creada por flask-migrate
│
├── tests/                 # pruebas con pytest
│   ├── conftest.py
│   └── test_auth.py
│
├── config.py              # configuración general
├── run.py                 # punto de entrada
├── requirements.txt
└── venv/




















#===================================================
PARA INSTALAR DEPENDENCIAS Y LIBRERIAS:

Para instalar todo: pip install -r requirements.txt

#===================================================
PARA ENTRAR A LA BASE DE DATOS:

Para ingresar a la DDBB de mysql: 
    desde consola: 
        $ sudo mysql -u root -p: ---> contraseña del sistema ( windows, linux, o mac )
        $ Enter password: JadenKugo2119$&? ( contraseña para ingresar a la DDBB: ddbb_antares_project )

Seleccionar DDBB: $ use ddbb_antares_project; ( y listo estamos dentro de la base de datos )



#===================================================
PARA ESTAS DENTRO DE LA DDBB DE FIREBASE: 


Desde el file: .env = ( contenido ):



# MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=JadenKugo2119$&?
DB_NAME=ddbb_antares_project

# Firebase
FIREBASE_CRED_PATH=/home/jaden9112/Escritorio/pro-ant/firebase/clave_privada.json
FIREBASE_DB_URL=https://antares-academy-default-rtdb.firebaseio.com/


FIREBASE_BUCKET_URL=gs://antares-academy.firebasestorage.app

# Clave_Privada (de firebase ) :




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

