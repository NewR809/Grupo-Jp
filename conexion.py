# Importaciones
import os, mysql.connector
import mysql.connector
from mysql.connector import pooling
from config import DB_CONFIG



def crear_conexion():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "gondola.proxy.rlwy.net"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "DKdNBPtQrzWVwArUWDqIFKEzbSnQIvlG"),
        database=os.getenv("DB_NAME", "railway")
    )


def guardar_en_mysql(tabla, datos):
    conn = crear_conexion()   # Obtiene una conexión del pool
    cur = conn.cursor()
    if tabla == "Gastos":
        sql = "INSERT INTO gastos (fecha, usuario, monto, categoria, descripcion) VALUES (%s, %s, %s, %s, %s)"
    else:
        sql = "INSERT INTO ingresos (fecha, usuario, monto, fuente, descripcion) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, datos)
    conn.commit()
    cur.close()
    conn.close()  # 👈 Devuelve la conexión al pool

# conexion.py
from mysql.connector import pooling
from config import DB_CONFIG

# Crear un pool de conexiones reutilizables
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,   # Ajusta según la carga
    **DB_CONFIG
)

def crear_conexion():
    """
    Obtiene una conexión desde el pool.
    Recuerda cerrar la conexión con .close() después de usarla.
    """
    return connection_pool.get_connection()