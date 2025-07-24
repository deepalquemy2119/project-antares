# project-antares

Estructura del proyecto:

project-antares/
├── .env
├── .gitignore
├── LICENSE
├── Dockerfile.test
├── README.md
├── config.py
├── requirements.txt
├── res/.txt
├── run.py
├── pytest.ini
├── seed_and_sync.py

├── app/
│   ├── __init__.py
│   ├── controllers/
│   ├── models/models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin_routes.py
│   │   ├── auth_routes.py
│   │   ├── course_routes.py
│   │   ├── public_routes.py
│   │   ├── tutor_routes.py
│   │   └── user_routes.py
│   ├── services/
│   │   ├── __pycache__/
│   │   └── emailservice.py
│   ├── static/
│   │   ├── css/
│   │   ├── icons/
│   │   ├── img/
│   │   ├── js/
│   │   ├── auth/
│   │   ├── componentes/
│   │   ├── materials/
│   │   ├── tutor/
│   │   └── user/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── public.html
│   │   └── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── routes.py
│   ├── ddbb/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── ddbb.antares_projects.sql
│   │   ├── connection/
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__/
│   │   │   └── conector.py
│   ├── firebase/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── clave_privada.json
│   │   └── firebase_init.py
│   ├── logs/
│   ├── syne/
│   ├── utils/
│   │   └── sync_mysql_to_firebase.py
│   ├── tests/
│   └── uploads/

├── company/
├── venv/

#===================================================
Para instalar todo: pip install -r requirements.txt

