from flask import Flask, request, jsonify
from functools import wraps
from db import consultar_tabla, insertar_en_tabla

# --- Autenticación básica ---
def autenticar(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == "powerbi" and auth.password == "secure123"):
            return jsonify({"error": "No autorizado"}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- Crear app Flask ---
app = Flask(__name__)

# --- Ruta principal ---
@app.route("/")
def home():
    return "API para Power BI funcionando correctamente"

# --- Consultar gastos ---
@app.route("/consultar_gastos", methods=["GET"])
@autenticar
def consultar_gastos():
    try:
        resultados = consultar_tabla("Gastos")
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Consultar ingresos ---
@app.route("/consultar_ingresos", methods=["GET"])
@autenticar
def consultar_ingresos():
    try:
        resultados = consultar_tabla("Ingresos")
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Insertar gasto ---
@app.route("/insertar_gasto", methods=["POST"])
@autenticar
def insertar_gasto():
    try:
        datos = request.get_json()
        cliente_id = datos.get("cliente_id")
        dato = datos.get("dato")
        usuario = datos.get("usuario")
        monto = datos.get("monto")
        categoria = datos.get("categoria")
        descripcion = datos.get("descripcion")

        if not all([cliente_id, dato, usuario, monto, categoria, descripcion]):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        insertar_en_tabla("Gastos", cliente_id, dato, usuario, monto, categoria, descripcion)
        return jsonify({"mensaje": "Gasto registrado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Ejecutar servidor ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)