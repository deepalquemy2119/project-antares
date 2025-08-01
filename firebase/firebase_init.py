import os
import json
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

# Cargar variables del entorno (.env si es local)
load_dotenv()

firebase_db_url = os.getenv("FIREBASE_DB_URL")
firebase_key_json_env = os.getenv("FIREBASE_KEY_JSON")  # desde Railway
firebase_cred_path = os.getenv("FIREBASE_CRED_PATH", "./firebase/firebase-key.json")

# Verificación mínima
if not firebase_db_url:
    raise Exception("FIREBASE_DB_URL no está definida")

# Determinar credenciales
if firebase_key_json_env:
    # Preferido en producción: variable de entorno JSON
    cred_dict = json.loads(firebase_key_json_env)
    cred = credentials.Certificate(cred_dict)

elif os.path.exists(firebase_cred_path):
    # Fallback local: leer archivo
    with open(firebase_cred_path) as f:
        cred_dict = json.load(f)
    cred = credentials.Certificate(cred_dict)

else:
    raise Exception("No se encontraron credenciales de Firebase (ni FIREBASE_KEY_JSON ni archivo en FIREBASE_CRED_PATH)")

# Inicializar Firebase
firebase_admin.initialize_app(cred, {
    "databaseURL": firebase_db_url
})

def get_firebase_db():
    return db
