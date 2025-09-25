# ingresos_handler.py

from datetime import datetime
from tkinter import messagebox
from base_datos import guardar_en_mysql
from desktop.utils import guardar_csv, INGRESOS_FILE


def procesar_ingreso(usuario, monto_str, categoria, descripcion, ventana=None):
    if not monto_str:
        messagebox.showwarning("Entrada requerida", "Ingrese un monto")
        return

    try:
        monto = float(monto_str)
    except ValueError:
        messagebox.showwarning("Valor inválido", "El monto debe ser un número")
        return

    fecha = datetime.now().strftime("%Y-%m-%d")
    datos = [fecha, usuario, monto, categoria, descripcion]

    try:
        guardar_csv(INGRESOS_FILE, datos)
        guardar_en_mysql("ingresos", datos)
        print("✅ Ingreso procesado:", datos)
        messagebox.showinfo("Éxito", "Ingreso registrado exitosamente")
        if ventana:
            ventana.destroy()
    except Exception as e:
        print("❌ Error al procesar ingreso:", e)
        messagebox.showerror("Error", f"No se pudo registrar el ingreso:\n{e}")