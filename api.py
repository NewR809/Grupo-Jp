from flask import Flask, request, jsonify, render_template, redirect, url_for
from functools import wraps
import mysql.connector
from db import consultar_tabla, insertar_en_tabla
from config import USERNAME, PASSWORD, DB_CONFIG

# --- Autenticación básica ---
def autenticar(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == USERNAME and auth.password == PASSWORD):
            return jsonify({"error": "No autorizado"}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- Crear app Flask ---
app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ============================================================
# 🔑 Panel de Licencias en la raíz
# ============================================================

@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM licencias")
    licencias = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("panel.html", licencias=licencias)

# ============================================================
# 🔑 Endpoints de Licencias
# ============================================================

@app.route("/licencias/validar", methods=["GET"])
def validar_licencia():
    clave = request.args.get("clave")
    if not clave:
        return jsonify({"status": "error", "mensaje": "Falta la clave"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM licencias WHERE clave=%s AND activa=1", (clave,))
    licencia = cursor.fetchone()
    cursor.close()
    conn.close()

    if licencia:
        return jsonify({
            "status": "ok",
            "mensaje": "Licencia válida",
            "cliente": licencia["cliente"]
        }), 200
    else:
        return jsonify({"status": "error", "mensaje": "Licencia inválida o inactiva"}), 401

@app.route("/solicitar_licencia", methods=["POST"])
def solicitar_licencia():
    data = request.get_json(force=True)
    clave = data.get("clave")
    cliente = data.get("cliente")

    if not clave or not cliente:
        return jsonify({"status": "error", "mensaje": "Faltan datos"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO licencias (clave, cliente, activa) VALUES (%s, %s, 0)", (clave, cliente))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "ok", "mensaje": "Solicitud registrada, pendiente de aprobación"}), 201

@app.route("/activar/<int:licencia_id>")
def activar_licencia(licencia_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE licencias SET activa=1 WHERE id=%s", (licencia_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("home"))

@app.route("/desactivar/<int:licencia_id>")
def desactivar_licencia(licencia_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE licencias SET activa=0 WHERE id=%s", (licencia_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("home"))

# ============================================================
# 📊 Endpoints Financieros (sin cambios)
# ============================================================

@app.route("/consultar_gastos", methods=["GET"])
@autenticar
def consultar_gastos():
    try:
        resultados = consultar_tabla("gastos")
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/consultar_ingresos", methods=["GET"])
@autenticar
def consultar_ingresos():
    try:
        resultados = consultar_tabla("ingresos")
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/insertar_gasto", methods=["POST"])
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

@app.route("/insertar_ingreso", methods=["POST"])
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

@app.route("/datos", methods=["GET"])
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

# ============================================================
# 🔎 Consultas con filtros
# ============================================================

@app.route("/consultas", methods=["GET"])
def consultas():
    empresa = request.args.get("empresa")
    anio = request.args.get("anio")
    mes = request.args.get("mes")
    semana = request.args.get("semana")
    dia = request.args.get("dia")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query_gastos = "SELECT fecha, usuario, monto, categoria, descripcion FROM gastos WHERE 1=1"
    if empresa: query_gastos += f" AND usuario='{empresa}'"
    if anio: query_gastos += f" AND YEAR(fecha)={anio}"
    if mes: query_gastos += f" AND MONTH(fecha)={mes}"
    if semana: query_gastos += f" AND WEEK(fecha)={semana}"
    if dia: query_gastos += f" AND DAY(fecha)={dia}"
    cursor.execute(query_gastos)
    gastos = cursor.fetchall()

    query_ingresos = "SELECT fecha, usuario, monto, categoria, descripcion FROM ingresos WHERE 1=1"
    if empresa: query_ingresos += f" AND usuario='{empresa}'"
    if anio: query_ingresos += f" AND YEAR(fecha)={anio}"
    if mes: query_ingresos += f" AND MONTH(fecha)={mes}"
    if semana: query_ingresos += f" AND WEEK(fecha)={semana}"
    if dia: query_ingresos += f" AND DAY(fecha)={dia}"
    cursor.execute(query_ingresos)
    ingresos = cursor.fetchall()

    recurrente = []
    if empresa:
        if not mes:
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

    cursor.close()
    conn.close()

    return jsonify({
        "gastos": gastos,
        "ingresos": ingresos,
        "recurrente": recurrente
    })

# --- Punto de entrada ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)