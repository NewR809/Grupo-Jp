from conexion import crear_conexion
from tkinter import messagebox

def guardar_en_mysql(tabla, datos):
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()

        if tabla.lower() == "ingresos":
            query = """INSERT INTO ingresos (fecha, usuario, monto, categoria, descripcion)
                       VALUES (%s, %s, %s, %s, %s)"""
        elif tabla.lower() == "gastos":
            query = """INSERT INTO gastos (fecha, usuario, monto, categoria, descripcion)
                       VALUES (%s, %s, %s, %s, %s)"""
        else:
            raise ValueError("Tabla no válida")

        cursor.execute(query, tuple(datos))
        conexion.commit()
        cursor.close()
        conexion.close()
        print("✅ Ingreso guardados en MySQL:", datos)
    except Exception as e:
        print(f"❌ Error MySQL: ", e)
        from tkinter import messagebox
        messagebox.showerror("Error MySQL", str(e))