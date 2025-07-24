# from dotenv import load_dotenv
# import os

# load_dotenv()


# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'clave_por_defecto')  # usa variable de entorno o default inseguro

#     MYSQL_HOST = os.getenv("DB_HOST")
#     MYSQL_USER = os.getenv("DB_USER")
#     MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
#     MYSQL_DATABASE = os.getenv("DB_NAME")

#     # Construir la URI para SQLAlchemy usando los datos anteriores
#     SQLALCHEMY_DATABASE_URI = (
#         f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")
#     FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH")
    
#     CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
#     CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

#     # Mailtrap config para testing
#     MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
#     MAIL_PORT = 587
#     MAIL_USERNAME = os.getenv('MAILTRAP_USER')
#     MAIL_PASSWORD = os.getenv('MAILTRAP_PASS')
#     MAIL_USE_TLS = True
#     MAIL_USE_SSL = False


#////////////////////////////////////////////////////////////

# project-antares/config.py

import os
from dotenv import load_dotenv

# Cargamos variables del .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_por_defecto')  # clave por defecto insegura para dev

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

    # Base de datos
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

    # Mail (Mailtrap por defecto)
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv('MAILTRAP_USER')
    MAIL_PASSWORD = os.getenv('MAILTRAP_PASS')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

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
