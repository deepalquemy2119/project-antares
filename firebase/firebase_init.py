import os
import firebase_admin
from firebase_admin import credentials

# Ruta absoluta al archivo de credenciales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, 'clave_privada.json')

# Verifica si el archivo existe
if not os.path.exists(cred_path):
    raise FileNotFoundError(f"[ERROR] No se encontró la clave privada: {cred_path}")

# Inicializa Firebase
cred = credentials.Certificate(cred_path)
default_app = firebase_admin.initialize_app(cred)

# Por ejemplo, si usas Firestore:
from firebase_admin import firestore
db = firestore.client()

def get_firebase_db():
    return db
