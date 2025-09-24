import os
from mysql.connector import pooling

# --- Configuración DB ---
DB_CONFIG = {
    "host": os.getenv("MYSQLHOST", "gondola.proxy.rlwy.net"),
    "port": int(os.getenv("MYSQLPORT", 18615)),
    "user": os.getenv("MYSQLUSER", "root"),
    "password": os.getenv("MYSQLPASSWORD", "DKdNBPtQrzWVwArUWDqIFKEzbSnQIvlG"),
    "database": os.getenv("MYSQLDATABASE", "railway"),
    "charset": "utf8mb4"
}

# --- Pool de conexiones ---
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **DB_CONFIG
)

def definir_conexion():
    return connection_pool.get_connection()

# --- Credenciales API ---
USERNAME = os.getenv("API_USER", "powerbi")
PASSWORD = os.getenv("API_PASS", "secure123")