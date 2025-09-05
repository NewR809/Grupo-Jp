from flask import Blueprint, request, jsonify
from auth import autenticar
from db import insertar_en_tabla, consultar_tabla

gastos_bp = Blueprint("gastos", __name__)

@gastos_bp.route("/insertar_gasto", methods=["POST"])
@autenticar
def insertar_gasto():
    datos = request.get_json()
    cliente_id = datos.get("cliente_id")
    dato = datos.get("dato")
    if not cliente_id or not dato:
        return jsonify({"error": "Faltan campos requeridos"}), 400
    insertar_en_tabla("gastos", cliente_id, dato)
    return jsonify({"mensaje": "Gasto registrado correctamente"}), 200

@gastos_bp.route("/consultar_gastos", methods=["GET"])
@autenticar
def consultar_gastos():
    resultados = consultar_tabla("gastos")
    return jsonify(resultados), 200