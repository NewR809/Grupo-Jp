from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from servidor_de_licencias.license_store import LicenseStore
from servidor_de_licencias.config_server import DB_CONFIG

app = Flask(__name__)

auth = HTTPBasicAuth()
store = LicenseStore(DB_CONFIG)

def _query_ingresos(fecha_desde=None, fecha_hasta=None, cliente=None, page=1, page_size=50):
    conn = store._conn()
    try:
        cur = conn.cursor(dictionary=True)
        where = []
        params = []
        if fecha_desde:
            where.append("fecha >= %s")
            params.append(fecha_desde)
        if fecha_hasta:
            where.append("fecha <= %s")
            params.append(fecha_hasta)
        if cliente:
            where.append("usuario = %s")
            params.append(cliente)
        where_sql = ("WHERE " + " AND ".join(where)) if where else ""
        offset = (page - 1) * page_size
        sql = f"""
            SELECT fecha, usuario, monto, categoria, descripcion
            FROM ingresos
            {where_sql}
            ORDER BY fecha DESC
            LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        cur.execute(sql, params)
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()

def _query_gastos(fecha_desde=None, fecha_hasta=None, cliente=None, page=1, page_size=50):
    conn = store._conn()
    try:
        cur = conn.cursor(dictionary=True)
        where = []
        params = []
        if fecha_desde:
            where.append("fecha >= %s")
            params.append(fecha_desde)
        if fecha_hasta:
            where.append("fecha <= %s")
            params.append(fecha_hasta)
        if cliente:
            where.append("usuario = %s")
            params.append(cliente)
        where_sql = ("WHERE " + " AND ".join(where)) if where else ""
        offset = (page - 1) * page_size
        sql = f"""
            SELECT fecha, usuario, monto, categoria, descripcion
            FROM gastos
            {where_sql}
            ORDER BY fecha DESC
            LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        cur.execute(sql, params)
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()

@app.route("/reportes/ingresos", methods=["GET"])
@auth.login_required
def reportes_ingresos():
    # Filtros: ?desde=YYYY-MM-DD&hasta=YYYY-MM-DD&cliente=Nombre&page=1&page_size=50
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    cliente = request.args.get("cliente")
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 50)), 200)  # límite de seguridad
    try:
        data = _query_ingresos(desde, hasta, cliente, page, page_size)
        return jsonify({"status": "ok", "count": len(data), "data": data})
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500

@app.route("/reportes/gastos", methods=["GET"])
@auth.login_required
def reportes_gastos():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    cliente = request.args.get("cliente")
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 50)), 200)
    try:
        data = _query_gastos(desde, hasta, cliente, page, page_size)
        return jsonify({"status": "ok", "count": len(data), "data": data})
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500