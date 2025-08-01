

import os
from dotenv import load_dotenv

# Cargamos variables del .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_por_defecto')

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
   

    # Base de datos
    MYSQL_PORT = os.getenv("DB_PORT", 3306)
    MYSQL_HOST = os.getenv("DB_HOST")
    MYSQL_USER = os.getenv("DB_USER")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
    MYSQL_DATABASE = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Firebase
    FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")
    FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH")

    # Celery
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

  # Mail (Gmail con contraseña de aplicación)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv('GMAIL_USER')
    MAIL_PASSWORD = os.getenv('GMAIL_APP_PASS')  # contraseña de aplicación
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@antares.com')


    # Carpeta de subida de archivos
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/test_db'
    FIREBASE_DB_URL = 'https://<tu-test-url>.firebaseio.com/'
    FIREBASE_CRED_PATH = '/firebase/clave_privada.json'


# --------- Para subir materiales para crear Cursos ----- viene de app/_init_.py ------
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:password@localhost/ddbb_antares_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
