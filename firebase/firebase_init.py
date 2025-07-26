# import os
# import firebase_admin
# from firebase_admin import credentials

# # Ruta absoluta al archivo de credenciales
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# cred_path = os.path.join(BASE_DIR, 'clave_privada.json')

# # Verifica si el archivo existe
# if not os.path.exists(cred_path):
#     raise FileNotFoundError(f"[ERROR] No se encontró la clave privada: {cred_path}")

# # Inicializa Firebase
# cred = credentials.Certificate(cred_path)
# default_app = firebase_admin.initialize_app(cred)

# # Por ejemplo, si usas Firestore:
# from firebase_admin import firestore
# db = firestore.client()

# def get_firebase_db():
#     return db





#/////////////////    Esto si usamos FireStore    ////////////////////////

# import os
# import json
# import firebase_admin
# from firebase_admin import credentials, firestore

# def get_firebase_db():
#     if not firebase_admin._apps:
#         cred_json = os.getenv('FIREBASE_CRED_JSON')
#         if not cred_json:
#             raise ValueError("[ERROR] La variable de entorno FIREBASE_CRED_JSON no está definida.")

#         try:
#             cred_dict = json.loads(cred_json)
#             cred = credentials.Certificate(cred_dict)
#             firebase_admin.initialize_app(cred)
#         except Exception as e:
#             raise RuntimeError(f"[ERROR] Falló la inicialización de Firebase: {e}")

#     return firestore.client()


# ///////////////// Si usamos RTDB en firebase ///////////////////

# import os
# import json
# import firebase_admin
# from firebase_admin import credentials, db as rtdb  # usamos RTDB

# # 🔐 Tomar el JSON de la clave desde la variable de entorno
# firebase_cred_raw = os.getenv('FIREBASE_CRED_JSON')

# if not firebase_cred_raw:
#     raise ValueError("[ERROR] No se encontró la variable de entorno FIREBASE_CRED_JSON")

# # Convertir el JSON string a diccionario
# firebase_cred_dict = json.loads(firebase_cred_raw)

# # Inicializar Firebase con la credencial y la URL de RTDB
# cred = credentials.Certificate(firebase_cred_dict)
# firebase_admin.initialize_app(cred, {
#     'databaseURL': os.getenv('FIREBASE_DB_URL')  # también desde entorno
# })

# # Retornar el cliente de RTDB
# def get_firebase_db():
#     return rtdb

#===============  Con variables de Entorno  ==================

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
