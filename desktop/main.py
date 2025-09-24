from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "powerbi": "secure123"
}

@auth.verify_password
def verify_password(username, password):
    return users.get(username) == password

@app.route('/insertar', methods=['POST'])
@auth.login_required
def insertar():
    data = request.get_json()
    cliente_id = data.get("cliente_id")
    dato = data.get("dato")
    print(f"Datos recibidos de {cliente_id}: {dato}")
    return jsonify({"mensaje": "Datos recibidos correctamente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)