# license_store.py
import mysql.connector
from contextlib import closing
from datetime import datetime
#from config import DB_CONFIG  # 👈 asegúrate de tener DB_CONFIG en config.py con tus credenciales Railway
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DB_CONFIG

class LicenseStore:
    def __init__(self,DB_CONFIG):
        self.DB_CONFIG = DB_CONFIG
        self._init_db()

    def _conn(self):
        return mysql.connector.connect(**DB_CONFIG)

    def _init_db(self):
        with closing(self._conn()) as conn:
            cur = conn.cursor()
            # Tabla de dispositivos
            cur.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    device_id VARCHAR(255) PRIMARY KEY,
                    alias VARCHAR(255),
                    usuario VARCHAR(255),
                    estado ENUM('activo','inactivo') NOT NULL DEFAULT 'inactivo',
                    registered_at DATETIME NOT NULL
                )
            """)
            # Tabla de auditoría
            cur.execute("""
                CREATE TABLE IF NOT EXISTS audits (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    device_id VARCHAR(255),
                    action VARCHAR(255),
                    ts DATETIME NOT NULL
                )
            """)
            # Tabla de usuarios
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role ENUM('visor','admin') NOT NULL
                )
            """)
            # Crear usuario inicial "visor" si no existe
            cur.execute("SELECT 1 FROM usuarios WHERE username=%s", ("visor",))
            if not cur.fetchone():
                cur.execute("INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)",
                            ("visor", "visorsecret", "visor"))
            conn.commit()

    # ------------------- Gestión de dispositivos -------------------

    def register_device(self, device_id: str, alias: str | None, usuario: str | None):
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with closing(self._conn()) as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM devices WHERE device_id=%s", (device_id,))
            exists = cur.fetchone() is not None
            if exists:
                cur.execute("UPDATE devices SET alias=%s, usuario=%s WHERE device_id=%s",
                            (alias, usuario, device_id))
            else:
                cur.execute("""
                    INSERT INTO devices (device_id, alias, usuario, estado, registered_at)
                    VALUES (%s, %s, %s, 'inactivo', %s)
                """, (device_id, alias, usuario, now))
            cur.execute("INSERT INTO audits (device_id, action, ts) VALUES (%s, %s, %s)",
                        (device_id, "register", now))
            conn.commit()

    def set_state(self, device_id: str, estado: str):
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with closing(self._conn()) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE devices SET estado=%s WHERE device_id=%s", (estado, device_id))
            cur.execute("INSERT INTO audits (device_id, action, ts) VALUES (%s, %s, %s)",
                        (device_id, f"set:{estado}", now))
            conn.commit()

    def verify(self, device_id: str) -> bool:
        with closing(self._conn()) as conn:
            cur = conn.cursor()
            cur.execute("SELECT estado FROM devices WHERE device_id=%s", (device_id,))
            row = cur.fetchone()
            return bool(row and row[0] == "activo")

    def list_devices(self):
        with closing(self._conn()) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT device_id, alias, usuario, estado, registered_at
                FROM devices ORDER BY registered_at DESC
            """)
            cols = ["device_id","alias","usuario","estado","registered_at"]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

    def audits(self, device_id: str | None = None):
        with closing(self._conn()) as conn:
            cur = conn.cursor()
            if device_id:
                cur.execute("""
                    SELECT id, device_id, action, ts
                    FROM audits WHERE device_id=%s ORDER BY ts DESC
                """, (device_id,))
            else:
                cur.execute("SELECT id, device_id, action, ts FROM audits ORDER BY ts DESC")
            cols = ["id","device_id","action","ts"]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

    # ------------------- Gestión de usuarios -------------------

    def create_user(self, username: str, password: str, role: str):
        with closing(self._conn()) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)",
                        (username, password, role))
            conn.commit()

    def list_users(self):
        with closing(self._conn()) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, username, role FROM usuarios ORDER BY id ASC")
            cols = ["id","username","role"]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

    def get_user(self, username: str):
        with closing(self._conn()) as conn:
            cur = conn.cursor()
            cur.execute("SELECT username, password, role FROM usuarios WHERE username=%s", (username,))
            row = cur.fetchone()
            if row:
                return {"username": row[0], "password": row[1], "role": row[2]}
            return None