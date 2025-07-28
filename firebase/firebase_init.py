

import os
import json
import firebase_admin
from firebase_admin import credentials, db

from dotenv import load_dotenv
load_dotenv()

# Obtener las variables desde el entorno
firebase_db_url = os.getenv("FIREBASE_DB_URL")
firebase_cred_path = os.getenv("FIREBASE_CRED_PATH")

if not firebase_db_url or not firebase_cred_path:
    raise Exception("FIREBASE_DB_URL y/o FIREBASE_CRED_PATH no están configuradas")




with open(firebase_cred_path) as f:
    cred_dict = json.load(f)

# Inicializar app de Firebase
cred = credentials.Certificate(cred_dict)
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': firebase_db_url
})

# Obtener referencia al RTDB
def get_firebase_db():
    return db
