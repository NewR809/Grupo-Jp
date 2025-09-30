from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from api_blueprint import  powerbi_bp   # Blueprint de Power BI
from api import  licenses_bp            # Blueprint de licencias y finanzas



# --- Crear aplicación principal ---
app = Flask(__name__)
auth = HTTPBasicAuth()

# --- Usuarios autorizados ---
users = {
    "powerbi": "secure123"
}



import os

#@app.before_request
#def mostrar_templates_info():
ruta = os.path.join(os.path.dirname(__file__), "templates")
if os.path.exists(ruta):
        print("📂 Flask buscará plantillas en:", ruta)
        print("📄 Archivos dentro:", os.listdir(ruta))
else:
        print("❌ Carpeta templates NO encontrada")



import os

#@app.before_first_request
#def verificar_templates():
ruta = os.path.join(os.path.dirname(__file__), "templates")
print("📂 Flask buscará plantillas en:", ruta)
if os.path.exists(ruta):
        print("✅ Carpeta templates encontrada")
        print("📄 Archivos dentro:", os.listdir(ruta))
else:
        print("❌ Carpeta templates NO encontrada")
# --- Registrar blueprints ---
app.register_blueprint(powerbi_bp)
app.register_blueprint(licenses_bp)

# --- Autenticación básica con HTTPBasicAuth ---
@auth.verify_password
def verify_password(username, password):
    return users.get(username) == password

import os

#@app.before_first_request
def verificar_templates():
    ruta = os.path.join(os.path.dirname(__file__), "templates")
    print("📂 Flask buscará plantillas en:", ruta)
    if os.path.exists(ruta):
        print("✅ Carpeta templates encontrada")
        print("📄 Archivos dentro:", os.listdir(ruta))
    else:
        print("❌ Carpeta templates NO encontrada")

# --- Ruta adicional de ejemplo ---
@app.route('/insertar', methods=['POST'])
@auth.login_required
def insertar():
    data = request.get_json()
    cliente_id = data.get("cliente_id")
    dato = data.get("dato")
    print(f"Datos recibidos de {cliente_id}: {dato}")
    return jsonify({"mensaje": "Datos recibidos correctamente"}), 200

@app.route("/")
def home():
    return """
    <h1>🚀 Servidor Grupo JP</h1>
    <p>El servidor está activo y funcionando.</p>
    <ul>
        <li><a href='/api/'>Panel de Licencias</a></li>
        <li><a href='/api/licencias/validar?clave=TEST123'>Validar Licencia (ejemplo)</a></li>
        <li><a href='/api/consultas?empresa=Tpack&anio=2025&mes=9'>Consultas (ejemplo)</a></li>
    </ul>
    """

# --- Punto de entrada ---
if __name__ == "__main__":
    # Para desarrollo local
    app.run(host='0.0.0.0', port=5000, debug=True)