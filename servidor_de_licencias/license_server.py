from flask import Flask, request, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import os

# Importa configuración y credenciales desde config_server
from servidor_de_licencias.config_server import (
    ADMIN_USERNAME,
    ADMIN_PASSWORD,
    VISOR_USERNAME,
    VISOR_PASSWORD,
    DB_CONFIG
)

from servidor_de_licencias.license_store import LicenseStore
from api_blueprint import api_bp   # 👈 Importamos el Blueprint de la API

# Inicializa Flask y autenticación
app = Flask(__name__)
auth = HTTPBasicAuth()

# Registrar el Blueprint de la API bajo /api
app.register_blueprint(api_bp)

# Inicializa la capa de almacenamiento con MySQL en Railway
store = LicenseStore(DB_CONFIG)

# Usuarios y roles
USERS = {
    ADMIN_USERNAME: {"password": ADMIN_PASSWORD, "role": "admin"},
    VISOR_USERNAME: {"password": VISOR_PASSWORD, "role": "visor"}
}

# 👇 Validación de credenciales
@auth.verify_password
def verify_password(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return username
    return None

def get_user_roles(username):
    user = USERS.get(username)
    if user:
        return user.get("role")
    return None

# ------------------- Rutas del panel -------------------

@app.route("/panel/devices", methods=["GET"])
@auth.login_required
def panel_devices():
    current_role = get_user_roles(auth.current_user())
    if current_role not in ("admin", "visor"):
        return "No autorizado", 403
    devices = store.list_devices()
    return render_template("devices.html", devices=devices, role=current_role, title="Panel de Dispositivos")

@app.route("/panel/register", methods=["POST"])
@auth.login_required
def register_device():
    current_role = get_user_roles(auth.current_user())
    if current_role not in ("admin", "visor"):
        return "No autorizado", 403
    device_id = request.form.get("device_id")
    alias = request.form.get("alias")
    usuario = request.form.get("usuario")
    if device_id:
        store.register_device(device_id, alias, usuario)
    return redirect(url_for("panel_devices"))

@app.route("/panel/toggle", methods=["POST"])
@auth.login_required
def panel_toggle():
    current_role = get_user_roles(auth.current_user())
    if current_role != "visor":
        return "No autorizado", 403
    device_id = request.form.get("device_id")
    estado = request.form.get("estado")
    if device_id and estado in ("activo", "inactivo"):
        store.set_state(device_id, estado)
    return redirect(url_for("panel_devices"))

@app.route("/panel/users", methods=["GET", "POST"])
@auth.login_required
def manage_users():
    current_role = get_user_roles(auth.current_user())
    if current_role != "visor":
        return "No autorizado", 403
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        new_role = request.form.get("role")
        if username and password and new_role in ("admin", "visor"):
            USERS[username] = {"password": password, "role": new_role}
    return render_template("users.html", users=USERS, title="Gestión de Usuarios")

# ------------------- Punto de entrada -------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)