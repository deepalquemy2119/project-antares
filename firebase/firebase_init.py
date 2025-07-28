

import os
import json
import firebase_admin
from firebase_admin import credentials, db

# Obtener las variables desde el entorno
firebase_db_url = os.getenv("FIREBASE_DB_URL")
firebase_cred_json = os.getenv("FIREBASE_CRED_JSON")

if not firebase_db_url or not firebase_cred_json:
    raise Exception("FIREBASE_DB_URL y/o FIREBASE_CRED_JSON no están configuradas")

# Convertir el string JSON a dict
cred_dict = json.loads(firebase_cred_json)

# Inicializar app de Firebase
cred = credentials.Certificate(cred_dict)
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': firebase_db_url
})

# Obtener referencia al RTDB
def get_firebase_db():
    return db
