from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from functools import wraps
import mysql.connector
import os
from db import consultar_tabla, insertar_en_tabla
from config import USERNAME, PASSWORD, DB_CONFIG
from servidor_de_licencias.license_store import LicenseStore

# --- Inicializar store ---
store = LicenseStore()

# --- Crear Blueprint ---
licenses_bp = Blueprint("licenses", __name__, url_prefix="/api")

# --- Autenticación básica ---
def autenticar(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == USERNAME and auth.password == PASSWORD):
            return jsonify({"error": "No autorizado"}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- Conexión a la base de datos ---
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ============================================================
# 🖥️ Panel de Dispositivos (con DB real)
# ============================================================

@licenses_bp.route("/panel/devices", methods=["GET"])
def panel_devices():
    devices = store.list_devices()  # obtiene lista real desde MySQL
    return render_template("devices.html", devices=devices)

@licenses_bp.route("/panel/register", methods=["POST"])
def register_device():
    device_id = request.form.get("device_id")
    alias = request.form.get("alias")
    usuario = request.form.get("usuario")
    if device_id:
        store.register_device(device_id, alias, usuario)  # guarda en DB
    return redirect(url_for("licenses.panel_devices"))

@licenses_bp.route("/panel/toggle", methods=["POST"])
def panel_toggle():
    device_id = request.form.get("device_id")
    estado = request.form.get("estado")
    if device_id and estado in ("activo", "inactivo"):
        store.set_state(device_id, estado)  # actualiza en DB
    return redirect(url_for("licenses.panel_devices"))


# ============================================================
# 🔑 Panel de Licencias en la raíz del blueprint
# ============================================================

@licenses_bp.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM licencias")
    licencias = cursor.fetchall()
    cursor.close()
    conn.close()
    print("plantillas buscadas en:", os.path.abspath("templates"))
    return render_template("panel.html", licencias=licencias)
    #return render_template("panel.html", licencias=licencias)

# ============================================================
# 🔑 Endpoints de Licencias
# ============================================================

@licenses_bp.route("/licencias/validar", methods=["GET"])
def validar_licencia():
    clave = request.args.get("clave")
    if not clave:
        return jsonify({"status": "error", "mensaje": "Falta la clave"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM licencias WHERE clave=%s", (clave,))
    licencia = cursor.fetchone()
    cursor.close()
    conn.close()

    if not licencia:
        return jsonify({"status": "error", "mensaje": "Licencia no encontrada"}), 404
    if not licencia["activa"]:
        return jsonify({"status": "pendiente", "mensaje": "Licencia pendiente de aprobación"}), 403

    return jsonify({
        "status": "ok",
        "mensaje": "Licencia válida",
        "cliente": licencia["cliente"]
    }), 200
    

@licenses_bp.route("/solicitar_licencia", methods=["POST"])
def solicitar_licencia():
    data = request.get_json(silent=True) or request.form
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

    # Si vino desde el panel (formulario HTML), redirige al panel
    if request.form:
        return redirect(url_for("licenses.home"))

    # Si vino como JSON (cliente remoto), responde JSON
    return jsonify({"status": "ok", "mensaje": "Solicitud registrada, pendiente de aprobación"}), 201

@licenses_bp.route("/activar/<int:licencia_id>")
def activar_licencia(licencia_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE licencias SET activa=1 WHERE id=%s", (licencia_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("licenses.home"))

@licenses_bp.route("/desactivar/<int:licencia_id>")
def desactivar_licencia(licencia_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE licencias SET activa=0 WHERE id=%s", (licencia_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("licenses.home"))

# ============================================================
# 📊 Endpoints Financieros
# ============================================================

@licenses_bp.route("/consultar_gastos", methods=["GET"])
@autenticar
def consultar_gastos():
    try:
        resultados = consultar_tabla("gastos")
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@licenses_bp.route("/consultar_ingresos", methods=["GET"])
@autenticar
def consultar_ingresos():
    try:
        resultados = consultar_tabla("ingresos")
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@licenses_bp.route("/insertar_gasto", methods=["POST"])
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

@licenses_bp.route("/insertar_ingreso", methods=["POST"])
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

@licenses_bp.route("/datos", methods=["GET"])
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
# 🔎 Consultas con filtros (versión robusta)
# ============================================================

@licenses_bp.route("/consultas", methods=["GET"])
def consultas():
    # empresa = usuario
    usuario = request.args.get("empresa")
    anio = request.args.get("anio")
    mes = request.args.get("mes")
    dia = request.args.get("dia")

    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        # --- Construcción segura de filtros ---
        filtros = []
        valores = []

        if usuario and usuario.strip():
            filtros.append("usuario = %s")
            valores.append(usuario.strip())

        if anio and anio.isdigit():
            filtros.append("YEAR(fecha) = %s")
            valores.append(int(anio))

        if mes and mes.isdigit():
            filtros.append("MONTH(fecha) = %s")
            valores.append(int(mes))

        if dia and dia.isdigit():
            filtros.append("DAY(fecha) = %s")
            valores.append(int(dia))

        where_clause = " AND ".join(filtros) if filtros else "1=1"

        # --- Consultas SQL explícitas ---
        sql_gastos = f"""
            SELECT id, usuario, fecha, monto, categoria, descripcion
            FROM gastos
            WHERE {where_clause}
        """
        sql_ingresos = f"""
            SELECT id, usuario, fecha, monto, categoria, descripcion
            FROM ingresos
            WHERE {where_clause}
        """

        print("DEBUG SQL:", sql_gastos, valores)

        cur.execute(sql_gastos, valores)
        gastos = cur.fetchall()

        cur.execute(sql_ingresos, valores)
        ingresos = cur.fetchall()

        # --- Gasto recurrente ---
        recurrente = []
        if mes and mes.isdigit():
            sql_recurrente = f"""
                SELECT MONTH(fecha, '%M') AS mes, categoria, COUNT(*) AS repeticiones
                FROM gastos
                WHERE {where_clause}
                GROUP BY mes, categoria
                ORDER BY repeticiones DESC
                LIMIT 5
            """
            cur.execute(sql_recurrente, valores)
            recurrente = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            "gastos": gastos,
            "ingresos": ingresos,
            "recurrente": recurrente
        }), 200

    except Exception as e:
        print("❌ Error en /consultas:", e)
        return jsonify({"error": str(e)}), 500
    
    # ============================================================
# 👤 Gestión de Usuarios
# ============================================================

@licenses_bp.route("/panel/users", methods=["GET", "POST"])
def manage_users():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role", "visor")
        if username and password:
            store.create_user(username, password, role)
    users = store.list_users()
    return render_template("users.html", users=users)