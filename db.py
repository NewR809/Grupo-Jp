#actualizarcion de la base de datos mysql a mysql_native_password
#numeor 2

from conexion import crear_conexion
#from tkinter import messagebox

from conexion import crear_conexion

# --- Insertar en tabla ---
def insertar_en_tabla(nombre_tabla, cliente_id, dato, usuario, monto, categoria, descripcion):
    conn = None
    cur = None
    try:
        if nombre_tabla.lower() not in ["gastos", "ingresos"]:
            raise ValueError(f"Tabla no soportada: {nombre_tabla}")

        conn = crear_conexion()
        cur = conn.cursor()
        query = f"""
            INSERT INTO {nombre_tabla} (cliente_id, dato, fecha, usuario, monto, categoria, descripcion)
            VALUES (%s, %s, CURDATE(), %s, %s, %s, %s)
        """
        valores = (cliente_id, dato, usuario, monto, categoria, descripcion)
        cur.execute(query, valores)
        conn.commit()
        print(f"✅ Registro insertado en {nombre_tabla}: {valores}")
    except Exception as e:
        print(f"❌ Error al insertar en {nombre_tabla}:", e)
        if conn:
            conn.rollback()
        raise   # 👈 importante: propagar el error a la API
    finally:
        if cur: cur.close()
        if conn: conn.close()

# --- Consultar tabla ---
def consultar_tabla(tabla):
    conn = None
    cur = None
    try:
        if tabla.lower() not in ["gastos", "ingresos"]:
            raise ValueError(f"Tabla no soportada: {tabla}")

        conn = crear_conexion()
        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM {tabla}")
        resultados = cur.fetchall()
        print(f"📊 {len(resultados)} registros obtenidos de {tabla}")
        return resultados
    except Exception as e:
        print(f"❌ Error al consultar {tabla}:", e)
        return []
    finally:
        if cur: cur.close()
        if conn: conn.close()

# --- Guardar en MySQL ---
def guardar_en_mysql(tabla, datos):
    conn = None
    cur = None
    try:
        conn = crear_conexion()
        cur = conn.cursor()

        if tabla.lower() == "gastos":
            query = """
                INSERT INTO gastos (fecha, usuario, monto, categoria, descripcion)
                VALUES (%s, %s, %s, %s, %s)
            """
        elif tabla.lower() == "ingresos":
            query = """
                INSERT INTO ingresos (fecha, usuario, monto, categoria, descripcion)
                VALUES (%s, %s, %s, %s, %s)
            """
        else:
            raise ValueError(f"Tabla no soportada: {tabla}")

        cur.execute(query, datos)
        conn.commit()
        print(f"✅ Datos guardados en {tabla}: {datos}")
    except Exception as e:
        print(f"❌ Error al guardar en {tabla}:", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if cur: cur.close()
        if conn: conn.close()