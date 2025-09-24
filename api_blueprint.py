from flask import Blueprint, request, jsonify
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

# --- Crear Blueprint ---
api_bp = Blueprint("api", __name__, url_prefix="/api")

# --- Ruta principal ---
@api_bp.route("/")
def home():
    return "API para Power BI funcionando correctamente"

# --- Consultar gastos ---
@api_bp.route("/consultar_gastos", methods=["GET"])
@autenticar
def consultar_gastos():
    try:
        resultados = consultar_tabla("Gastos")
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Consultar ingresos ---
@api_bp.route("/consultar_ingresos", methods=["GET"])
@autenticar
def consultar_ingresos():
    try:
        resultados = consultar_tabla("Ingresos")
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Insertar gasto ---
@api_bp.route("/insertar_gasto", methods=["POST"])
@autenticar
def insertar_gasto():
    try:
        data = request.get_json(force=True, silent=False)
        requerido = ["fecha", "categoria", "monto", "descripcion"]
        faltan = [k for k in requerido if k not in data]
        if faltan:
            return jsonify({"error": f"Faltan campos: {', '.join(faltan)}"}), 400

        insertar_en_tabla("Gastos", data)
        return jsonify({"mensaje": "Gasto insertado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Insertar ingreso ---
@api_bp.route("/insertar_ingreso", methods=["POST"])
@autenticar
def insertar_ingreso():
    try:
        data = request.get_json(force=True, silent=False)
        requerido = ["fecha", "categoria", "monto", "descripcion"]
        faltan = [k for k in requerido if k not in data]
        if faltan:
            return jsonify({"error": f"Faltan campos: {', '.join(faltan)}"}), 400

        insertar_en_tabla("Ingresos", data)
        return jsonify({"mensaje": "Ingreso insertado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Endpoint combinado para Power BI ---
@api_bp.route("/datos", methods=["GET"])
@autenticar
def datos():
    try:
        gastos = consultar_tabla("Gastos")
        ingresos = consultar_tabla("Ingresos")
        return jsonify({
            "Gastos": gastos,
            "Ingresos": ingresos
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500