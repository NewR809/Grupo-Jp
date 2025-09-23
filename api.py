from flask import Flask, request, jsonify
from functools import wraps
import mysql.connector
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

# --- Configuración DB para consultas ---
DB_CONFIG = {
    "host": "gondola.proxy.rlwy.net",
    "user": "root",
    "password": "DKdNBPtQrzWVwArUWDqIFKEzbSnQIvlG",
    "database": "railway",
    "port": 18615
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# --- Ruta principal ---
@app.route("/")
def home():
    return "API para Power BI y Consultas funcionando correctamente"

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
@app.route("/insertar_ingreso", methods=["POST"])
@autenticar
def insertar_ingreso():
    try:
        data = request.get_json(force=True, silent=False)
        requerido = ["fecha", "fuente", "monto", "descripcion"]
        faltan = [k for k in requerido if k not in data]
        if faltan:
            return jsonify({"error": f"Faltan campos: {', '.join(faltan)}"}), 400

        insertar_en_tabla("Ingresos", data)
        return jsonify({"mensaje": "Ingreso insertado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Endpoint para Power BI con tablas separadas ---
@app.route("/datos", methods=["GET"])
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

# --- NUEVO: Consultas con filtros y recurrente ---
@app.route("/consultas", methods=["GET"])
def consultas():
    empresa = request.args.get("empresa")
    anio = request.args.get("anio")
    mes = request.args.get("mes")
    semana = request.args.get("semana")
    dia = request.args.get("dia")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # --- Gastos ---
    query_gastos = "SELECT fecha, usuario, monto, categoria, descripcion FROM gastos WHERE 1=1"
    if empresa: query_gastos += f" AND usuario='{empresa}'"
    if anio: query_gastos += f" AND YEAR(fecha)={anio}"
    if mes: query_gastos += f" AND MONTH(fecha)={mes}"
    if semana: query_gastos += f" AND WEEK(fecha)={semana}"
    if dia: query_gastos += f" AND DAY(fecha)={dia}"
    cursor.execute(query_gastos)
    gastos = cursor.fetchall()

    # --- Ingresos ---
    query_ingresos = "SELECT fecha, usuario, monto, fuente, descripcion FROM ingresos WHERE 1=1"
    if empresa: query_ingresos += f" AND usuario='{empresa}'"
    if anio: query_ingresos += f" AND YEAR(fecha)={anio}"
    if mes: query_ingresos += f" AND MONTH(fecha)={mes}"
    if semana: query_ingresos += f" AND WEEK(fecha)={semana}"
    if dia: query_ingresos += f" AND DAY(fecha)={dia}"
    cursor.execute(query_ingresos)
    ingresos = cursor.fetchall()

    # --- Gasto más recurrente del mes ---
    recurrente = []
    if empresa:
        if not mes:  # si no se pasa mes, usar el actual
            cursor.execute("SELECT MONTH(CURDATE()) as mes_actual")
            mes = cursor.fetchone()["mes_actual"]

        cursor.execute(f"""
            SELECT categoria, COUNT(*) as repeticiones
            FROM gastos
            WHERE usuario='{empresa}' AND MONTH(fecha)={mes}
            GROUP BY categoria
            ORDER BY repeticiones DESC
            LIMIT 1
        """)
        recurrente = cursor.fetchall()

    conn.close()

    return jsonify({
        "gastos": gastos,
        "ingresos": ingresos,
        "recurrente": recurrente
    })

# --- Punto de entrada ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)