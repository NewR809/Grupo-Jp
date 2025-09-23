import csv
import os
import mysql.connector
from tkinter import messagebox

# --- Guardar en CSV ---
def guardar_csv(archivo, datos):
    try:
        with open(archivo, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(datos)
    except Exception as e:
        messagebox.showerror("Error al guardar CSV", str(e))

# --- Leer desde CSV ---
def leer_csv(archivo):
    if not os.path.exists(archivo):
        return []
    try:
        with open(archivo, mode='r', encoding='utf-8') as f:
            return list(csv.reader(f))
    except Exception as e:
        messagebox.showerror("Error al leer CSV", str(e))
        return []

# --- Guardar en MySQL (Railway) ---
def guardar_en_mysql(tabla, datos):
    try:
        conn = mysql.connector.connect(
            host="yamanote.proxy.rlwy.net",
            user="root",
            password="UyuZkiAaxFytvlevPCSrGMNPKhOeYxXT",
            database="railway"
        )
        cursor = conn.cursor()

        if tabla == "Gastos":
            query = "INSERT INTO gastos (fecha, usuario, monto, categoria, descripcion) VALUES (%s, %s, %s, %s, %s)"
        elif tabla == "Ingresos":
            query = "INSERT INTO ingresos (fecha, usuario, monto, fuente, descripcion) VALUES (%s, %s, %s, %s, %s)"
        else:
            messagebox.showerror("Tabla desconocida", f"No se reconoce la tabla: {tabla}")
            return

        cursor.execute(query, datos)
        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", f"No se pudo guardar en la base de datos:\n{err}")