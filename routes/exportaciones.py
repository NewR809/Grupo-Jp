from flask import Blueprint, jsonify, send_file
from auth import autenticar
from db import consultar_tabla
import pandas as pd

exportaciones_bp = Blueprint("exportaciones", __name__)

@exportaciones_bp.route("/descargar_ingresos", methods=["GET"])
@autenticar
def descargar_ingresos():
    df = pd.DataFrame(consultar_tabla("ingresos"))
    ruta = "datos_exportados/ingresos_exportados.csv"
    df.to_csv(ruta, index=False)
    return send_file(ruta, as_attachment=True)

@exportaciones_bp.route("/descargar_gastos", methods=["GET"])
@autenticar
def descargar_gastos():
    df = pd.DataFrame(consultar_tabla("gastos"))
    ruta = "datos_exportados/gastos_exportados.csv"
    df.to_csv(ruta, index=False)
    return send_file(ruta, as_attachment=True)