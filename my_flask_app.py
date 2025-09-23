# my_flask_app.py
from flask import Flask

app = Flask(__name__)

# Aquí defines tus rutas
@app.route("/")
def index():
    return "Hola, 🚀 tu app Flask está corriendo"