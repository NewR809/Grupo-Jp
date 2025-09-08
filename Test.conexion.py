from conexion import crear_conexion

def probar_conexion():
    try:
        conn = crear_conexion()
        print("✅ Conexión exitosa con Railway")
        conn.close()
    except Exception as e:
        print("❌ Error de conexión:", e)

if __name__ == "__main__":
    probar_conexion()