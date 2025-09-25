from flask import Blueprint, request, jsonify
from functools import wraps
from db import consultar_tabla, insertar_en_tabla

# --- Crear Blueprint ---
api_bp = Blueprint("api", __name__, url_prefix="/api")

# --- Autenticación básica ---
def autenticar(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == "powerbi" and auth.password == "secure123"):
            return jsonify({"error": "No autorizado"}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- Ruta principal ---
@api_bp.route("/")
def home():
    return jsonify({"mensaje": "API para Power BI funcionando correctamente"})

# --- Consultar gastos ---
@api_bp.route("/consultar_gastos", methods=["GET"])
@autenticar
def consultar_gastos():
    try:
        resultados = consultar_tabla("gastos")
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Consultar ingresos ---
@api_bp.route("/consultar_ingresos", methods=["GET"])
@autenticar
def consultar_ingresos():
    try:
        resultados = consultar_tabla("ingresos")
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

        insertar_en_tabla("gastos", data)
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

        insertar_en_tabla("ingresos", data)
        return jsonify({"mensaje": "Ingreso insertado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Endpoint combinado para Power BI ---
@api_bp.route("/datos", methods=["GET"])
@autenticar
def datos():
    try:
        gastos = consultar_tabla("gastos")
        ingresos = consultar_tabla("ingresos")
        return jsonify({
            "gastos": gastos,
            "ingresos": ingresos
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500