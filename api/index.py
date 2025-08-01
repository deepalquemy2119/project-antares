from run import app as handler

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensaje": "Hola desde Flask en Vercel"})

# Esto es obligatorio para que Vercel use app como handler
handler = app
