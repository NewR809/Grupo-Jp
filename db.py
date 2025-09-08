
from tkinter import messagebox

from config import DB_CONFIG



import mysql.connector

def crear_conexion():
    return mysql.connector.connect(
        host="yamanote.proxy.rlwy.net",
        user="root",
        password="UyuZkiAaxFytvlevPCSrGMNPKhOeYxXT",
        database="railway"
    )

def insertar_en_tabla(nombre_tabla, cliente_id, dato, usuario, monto, categoria, descripcion):
    conn = crear_conexion()
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
    cursor = conn.cursor(dictionary=True)  # ← devuelve diccionarios para JSON
    cursor.execute(f"SELECT * FROM {tabla}")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def guardar_en_mysql(tabla, datos):
    try:
        conn = mysql.connector.connect(
            host="yamanote.proxy.rlwy.net",
            user="root",
            password="UyuZkiAaxFytvlevPCSrGMNPKhOeYxXT",
            database="railway"
        )
        cursor = conn.cursor()
        query = f"""
            INSERT INTO {tabla} (fecha, usuario, monto, categoria, descripcion)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, datos)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error al guardar en MySQL", str(e))