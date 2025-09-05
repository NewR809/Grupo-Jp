import pymysql
from config import DB_CONFIG

def crear_conexion():
    return pymysql.connect(**DB_CONFIG)

def insertar_en_tabla(tabla, cliente_id, dato):
    conexion = crear_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {tabla} (cliente_id, dato) VALUES (%s, %s)",
            (cliente_id, dato)
        )
        conexion.commit()
    conexion.close()

def consultar_tabla(tabla):
    conexion = crear_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {tabla}")
        resultados = cursor.fetchall()
    conexion.close()
    return resultados