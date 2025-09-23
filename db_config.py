#actualizaciones realizadas en los archivos:
#db.py
from mysql.connector import pooling

# Configuración de conexión a Railway
DB_CONFIG = {
    "host": "gondola.proxy.rlwy.net",
    "port": 18615,
    "user": "root",
    "password": "DKdNBPtQrzWVwArUWDqIFKEzbSnQIvlG",
    "database": "railway",
    "charset": "utf8mb4"
}

# Crear un pool de conexiones reutilizables
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,   # Ajusta según la carga esperada
    **DB_CONFIG
)

def definir_conexion():
    """
    Obtiene una conexión desde el pool.
    Recuerda cerrar la conexión con .close() después de usarla.
    """
    return connection_pool.get_connection()

# Credenciales de autenticación para tu API
USERNAME = "powerbi"
PASSWORD = "secure123"