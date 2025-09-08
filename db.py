import os
import mysql.connector
from tkinter import messagebox

def crear_conexion():
    try:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "yamanote.proxy.rlwy.net"),
            port=int(os.environ.get("DB_PORT", 3306)),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", "UyuZkiAaxFytvlevPCSrGMNPKhOeYxXT"),
            database=os.environ.get("DB_NAME", "railway")
        )
    except Exception as e:
        print("❌ Error al conectar a MySQL:", e)
        try:
            messagebox.showerror("Error de conexión", str(e))
        except:
            pass
        return None

def insertar_en_tabla(nombre_tabla, cliente_id, dato, usuario, monto, categoria, descripcion):
    conn = crear_conexion()
    if not conn:
        return
    cursor = conn.cursor()
    query = f"""
        INSERT INTO {nombre_tabla} (cliente_id, dato, fecha, usuario, monto, categoria, descripcion)
        VALUES (%s, %s, CURDATE(), %s, %s, %s, %s)
    """
    valores = (cliente_id, dato, usuario, monto, categoria, descripcion)
    cursor.execute(query, valores)
    conn.commit()
    conn.close()

def consultar_tabla(tabla):
    conn = crear_conexion()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {tabla}")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def guardar_en_mysql(tabla, datos):
    conn = crear_conexion()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = f"""
            INSERT INTO {tabla} (fecha, usuario, monto, categoria, descripcion)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, datos)
        conn.commit()
        conn.close()
        print("✅ Datos guardados en MySQL:", datos)
    except Exception as e:
        print("❌ Error al guardar en MySQL:", e)
        try:
            messagebox.showerror("Error al guardar en MySQL", str(e))
        except:
            pass