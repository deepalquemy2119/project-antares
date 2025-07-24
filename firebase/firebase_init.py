import os
import firebase_admin
from firebase_admin import credentials, db, storage
from dotenv import load_dotenv

load_dotenv()






# Obtener ruta absoluta a la clave privada
cred_path = os.getenv("FIREBASE_CRED_PATH")
if not cred_path:
    cred_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "clave_privada.json"
    )

# Validar que el archivo exista
if not os.path.isfile(cred_path):
    raise FileNotFoundError(f"[ERROR] No se encontró la clave privada: {cred_path}")

# Obtener URL de la base de datos desde .env
db_url = os.getenv("FIREBASE_DB_URL")
bucket_url = os.getenv("FIREBASE_BUCKET_URL", "gs://antares-academy.firebasestorage.app")  # Valor por defecto

print(f"[DEBUG] cred_path: {cred_path}")
print(f"[DEBUG] db_url: {db_url}")
print(f"[DEBUG] bucket: {bucket_url}")

# Inicializar Firebase si no está ya inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': db_url,
        'storageBucket': bucket_url
    })

# Funciones utilitarias
def get_firebase_db():
    return db

def get_firebase_bucket():
    return storage.bucket()
