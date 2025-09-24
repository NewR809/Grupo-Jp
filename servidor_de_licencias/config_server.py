# servidor_de_licencias/config_server.py
import os

# Perfil admin (usuario con privilegios limitados)
ADMIN_USERNAME = os.getenv("LICENSE_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("LICENSE_ADMIN_PASS", "adminpass")

# Perfil visor (superusuario con control total)
VISOR_USERNAME = os.getenv("LICENSE_VISOR_USER", "visor")
VISOR_PASSWORD = os.getenv("LICENSE_VISOR_PASS", "visorsecret")

# Configuración de la base de datos MySQL en Railway
DB_CONFIG = {
    "host": os.getenv("MYSQLHOST", "gondola.proxy.rlwy.net"),
    "port": int(os.getenv("MYSQLPORT", 18615)),
    "user": os.getenv("MYSQLUSER", "root"),
    "password": os.getenv("MYSQLPASSWORD", "DKdNBPtQrzWVwArUWDqIFKEzbSnQIvlG"),
    "database": os.getenv("MYSQLDATABASE", "railway"),
}

# Alias para compatibilidad con tu código existente
DB_PATH = DB_CONFIG

# Validación opcional: si falta alguna variable crítica, lanza error
for key, value in DB_CONFIG.items():
    if value is None:
        raise RuntimeError(f"⚠️ Variable de entorno faltante: {key}")
