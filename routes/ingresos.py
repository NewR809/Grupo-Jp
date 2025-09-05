from flask import Blueprint, request, jsonify
from auth import autenticar
from db import insertar_en_tabla, consultar_tabla

ingresos_bp = Blueprint("ingresos", __name__)

@ingresos_bp.route("/insertar_ingreso", methods=["POST"])
@autenticar
def insertar_ingreso():
    datos = request.get_json()
    cliente_id = datos.get("cliente_id")
    dato = datos.get("dato")
    if not cliente_id or not dato:
        return jsonify({"error": "Faltan campos requeridos"}), 400
    insertar_en_tabla("ingresos", cliente_id, dato)
    return jsonify({"mensaje": "Ingreso registrado correctamente"}), 200

@ingresos_bp.route("/consultar_ingresos", methods=["GET"])
@autenticar
def consultar_ingresos():
    resultados = consultar_tabla("ingresos")
    return jsonify(resultados), 200