from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from api_blueprint import api_bp   # importa tu blueprint
#from licenses_blueprint import licenses_bp  # importa el blueprint de licencias
from api import api_bp as licenses_bp  # importa el blueprint de licencias
# --- Crear aplicación principal ---
app = Flask(__name__)
auth = HTTPBasicAuth()

# --- Usuarios autorizados ---
users = {
    "powerbi": "secure123"
}

# --- Registrar blueprint ---
app.register_blueprint(api_bp)
app.register_blueprint(licenses_bp)  # Registrar el blueprint de licencias

# --- Autenticación básica con HTTPBasicAuth ---
@auth.verify_password
def verify_password(username, password):
    return users.get(username) == password

# --- Ruta adicional de ejemplo ---
@app.route('/insertar', methods=['POST'])
@auth.login_required
def insertar():
    data = request.get_json()
    cliente_id = data.get("cliente_id")
    dato = data.get("dato")
    print(f"Datos recibidos de {cliente_id}: {dato}")
    return jsonify({"mensaje": "Datos recibidos correctamente"}), 200

# --- Punto de entrada ---
if __name__ == "__main__":
    # Para desarrollo local
    app.run(host='0.0.0.0', port=5000, debug=True)