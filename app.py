#IMPORTACIONES
import os
import csv
import pandas as pd
from datetime import datetime
from openpyxl.styles import Alignment, Font, PatternFill
import time
import sys
import ttkbootstrap as ttkbcliner
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog, Menu, Toplevel, StringVar, ttk, Entry, Text
from PIL import Image, ImageTk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import os
import sqlite3
import mysql.connector
from db import guardar_en_mysql
from conexion import crear_conexion
from base_datos import guardar_en_mysql
from base_datos import guardar_en_mysql
from archivos import guardar_csv, leer_csv




# --- Credenciales ---
usuarios = {
    "Henko01": "Hen4514",
    "Tpack": "Tpack4514",
    "JpSolar": "Jpsolar4514",
    "Quidopedia": "Qpd4514"
}
administrador = {
    "Admin": "Jpg4514"
}

nombres_usuarios = {
    "Henko01": "Usuario",
    "Tpack": "Usuario",
    "JpSolar": "Usuario",
    "Quidopedia": "Usuario",
    "Admin": "Gerente"
}
# --- Archivos ---
GASTOS_FILE = "gastos.csv"
INGRESOS_FILE = "ingresos.csv"
LOG_SESIONES = "log_sesiones.csv"
TIEMPO_MAX_INACTIVIDAD = 300  # segundos


# --- Utilidades de archivo ---
def guardar_csv(archivo, datos):
    with open(archivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(datos)

def leer_csv(archivo):
    if not os.path.exists(archivo):
        return []
    with open(archivo, mode='r', encoding='utf-8') as f:
        return list(csv.reader(f))

def ajustar_margenes_excel(writer, sheet_name, es_admin=False):
    ws = writer.sheets[sheet_name]
    color = "FFCCCC" if es_admin else "CCE5FF"
    for i in range(1, 4):
        for cell in ws[i]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws.column_dimensions[column].width = max_length + 2

def exportar_a_excel_consolidado(archivo_gastos, archivo_ingresos, archivo_excel, usuario_actual=None):
    # Función modificada para aceptar DataFrames en lugar de rutas de archivo
    def leer_o_usar_df(data):
        if isinstance(data, str) and os.path.exists(data):
            return pd.read_csv(data, header=None)
        elif isinstance(data, pd.DataFrame):
            return data
        return pd.DataFrame()

    df_gastos = leer_o_usar_df(archivo_gastos)
    df_ingresos = leer_o_usar_df(archivo_ingresos)
    
    if df_gastos.empty and df_ingresos.empty:
        messagebox.showerror("Error", "No hay datos para exportar.")
        return

    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    nombre_usuario = nombres_usuarios.get(usuario_actual, usuario_actual) if usuario_actual else "Sistema Financiero"
    es_admin = usuario_actual == "Admin"

    with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
        if not df_gastos.empty:
            encabezado_gastos = pd.DataFrame([[f"Exportado por: {nombre_usuario}", f"Fecha: {fecha_actual}"], ["Reporte: Gastos", ""]])
            encabezado_gastos.to_excel(writer, index=False, header=False, sheet_name="Gastos")
            df_gastos.columns = ["Fecha", "Usuario", "Monto", "Categoría/Fuente", "Descripción"]
            df_gastos.to_excel(writer, index=False, sheet_name="Gastos", startrow=3)
            ajustar_margenes_excel(writer, "Gastos", es_admin)

        if not df_ingresos.empty:
            encabezado_ingresos = pd.DataFrame([[f"Exportado por: {nombre_usuario}", f"Fecha: {fecha_actual}"], ["Reporte: Ingresos", ""]])
            encabezado_ingresos.to_excel(writer, index=False, header=False, sheet_name="Ingresos")
            df_ingresos.columns = ["Fecha", "Usuario", "Monto", "Categoría/Fuente", "Descripción"]
            df_ingresos.to_excel(writer, index=False, sheet_name="Ingresos", startrow=3)
            ajustar_margenes_excel(writer, "Ingresos", es_admin)

    messagebox.showinfo("Exportación exitosa", f"Archivo exportado como: {archivo_excel}")

# --- Vista previa antes de exportar ---
class VistaPrevia(tk.Toplevel):
    def __init__(self, master, gastos_df, ingresos_df, export_callback):
        super().__init__(master)
        self.title("Vista Previa Datos")
        self.geometry("900x500")
        self.export_callback = export_callback
        self.gastos_df = gastos_df
        self.ingresos_df = ingresos_df

        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill="both")

        self.tab_gastos = ttk.Frame(tab_control)
        tab_control.add(self.tab_gastos, text='Gastos')
        self.crear_treeview(self.tab_gastos, gastos_df)

        self.tab_ingresos = ttk.Frame(tab_control)
        tab_control.add(self.tab_ingresos, text='Ingresos')
        self.crear_treeview(self.tab_ingresos, ingresos_df)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Exportar", command=self.confirmar_exportacion).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side='left', padx=10)

    def crear_treeview(self, parent, df):
        cols = ["Fecha", "Usuario", "Monto", "Categoría/Fuente", "Descripción"]
        if not df.empty:
            df.columns = cols
        
        tree = ttk.Treeview(parent, columns=cols, show='headings')
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=150)
        tree.pack(expand=True, fill='both')

        if not df.empty:
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))
        return tree

    def confirmar_exportacion(self):
        self.export_callback()
        self.destroy()

# --- Registrar sesión ---
def registrar_log_sesion(usuario, tipo):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guardar_csv(LOG_SESIONES, [fecha_hora, usuario, tipo])

# --- Interfaz con ttkbootstrap ---
class SistemaFinancieroApp:
    def __init__(self, root):
        self.root = root
        self.usuario = "Admini"
        self.root.title("Sistema Financiero Empresarial")
        self.root.geometry("800x600")
        self.usuario = None
        self.tipo = None
        self.ultima_actividad = time.time()

        self.root.bind_all("<Any-KeyPress>", self.actualizar_actividad)
        self.root.bind_all("<Any-Button>", self.actualizar_actividad)
        self.root.after(10000, self.verificar_inactividad)

        self.crear_menu_barra()
        self.mostrar_login()

    def actualizar_actividad(self, event=None):
        self.ultima_actividad = time.time()

    def verificar_inactividad(self):
        if time.time() - self.ultima_actividad > TIEMPO_MAX_INACTIVIDAD:
            messagebox.showinfo("Sesión terminada", "Se cerró la sesión por inactividad.")
            self.mostrar_login()
        else:
            self.root.after(10000, self.verificar_inactividad)

    def crear_menu_barra(self):
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        self.menu_archivo = Menu(self.menubar, tearoff=0)
        self.menu_archivo.add_command(label="Cerrar sesión", command=self.mostrar_login)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=self.salir_app)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)

        # Limpiar menú de admin anterior si existe
        try:
            self.menubar.delete("Administración")
        except tk.TclError:
            pass
        
        if self.tipo == "admin":
            self.menu_admin = Menu(self.menubar, tearoff=0)
            self.menu_admin.add_command(label="Gestión de Empresas", command=self.gestion_empresas)
            self.menubar.add_cascade(label="Administración", menu=self.menu_admin)

    def salir_app(self):
        self.root.quit()
        sys.exit()

    def crear_barra_tareas(self):
        barra = ttkbcliner.Frame(self.root, bootstyle="dark")
        barra.pack(side="top", fill="x")

        titulo = ttkbcliner.Label(barra, text="💼 Sistema Financiero Empresarial", bootstyle="inverse-dark", font=("Segoe UI", 12, "bold"))
        titulo.pack(side="left", padx=15)

        usuario_label = ttkbcliner.Label(barra, text=f"👤 {self.usuario}", bootstyle="inverse-dark", font=("Segoe UI", 10))
        usuario_label.pack(side="right", padx=15)

    def mostrar_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.crear_menu_barra() # Recrear el menú base sin opciones de admin

        marco = ttkbcliner.Frame(self.root, padding=20)
        marco.pack(expand=True)

        ttkbcliner.Label(marco, text="Iniciar sesión", font=("Segoe UI", 14, "bold"), bootstyle="primary").pack(pady=10)
        self.usuario_entry = ttkbcliner.Entry(marco, width=30)
        self.usuario_entry.pack(pady=5)
        self.usuario_entry.insert(0, "Usuario")

        self.contrasena_entry = ttkbcliner.Entry(marco, show="*", width=30)
        self.contrasena_entry.pack(pady=5)
        self.contrasena_entry.insert(0, "")

        ttkbcliner.Button(marco, text="Entrar", bootstyle="success", command=self.login).pack(pady=20)

    def login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        if usuario in usuarios and usuarios[usuario] == contrasena:
            self.usuario, self.tipo = usuario, "usuario"
        elif usuario in administrador and administrador[usuario] == contrasena:
            self.usuario, self.tipo = usuario, "admin"
        else:
            messagebox.showerror("Error de login", "Credenciales incorrectas")
            return

        registrar_log_sesion(self.usuario, self.tipo)
        self.crear_menu_barra()  # actualizar menú si es admin
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.crear_barra_tareas()

        nombre = nombres_usuarios.get(self.usuario, self.usuario)
        ttkbcliner.Label(self.root, text=f"✅ Bienvenida a {self.usuario} ({nombre})", font=("Segoe UI", 12, "bold"), bootstyle="info").pack(pady=10)

        marco = ttkbcliner.Frame(self.root, padding=20)
        marco.pack()

        def crear_boton(texto, comando, estilo="primary"):
            ttkbcliner.Button(marco, text=texto, command=comando, bootstyle=estilo, width=35).pack(pady=5)

        if self.tipo == "admin":
            crear_boton("⚙️ Gestión de Empresas", self.gestion_empresas, "secondary")
            crear_boton("📤 Exportar todos los datos", self.mostrar_vista_previa_exportar, "warning")
            crear_boton("🕒 Ver historial de sesiones", self.ver_logs, "secondary")
        
        elif self.tipo == "usuario":
            crear_boton("🧾 Registrar Gasto", self.mostrar_menu_gastos, "danger")
            crear_boton("💰 Registrar Ingreso", self.mostrar_registrar_ingreso, "success")
            crear_boton("📊 Crear informe por período", self.mostrar_menu_exportacion_usuario, "info")
            crear_boton("📤 Exportar todos mis datos", self.exportar_todo_usuario_actual, "warning")

        ttkbcliner.Button(self.root, text="🔒 Cerrar sesión", command=self.mostrar_login, bootstyle="danger", width=35).pack(pady=20)

    def mostrar_menu_gastos(self):
        ventana = Toplevel(self.root)
        ventana.title("Registrar Gastos Detallados")
        ventana.geometry("600x500")

        notebook = ttk.Notebook(ventana)
        notebook.pack(expand=1, fill='both', padx=10, pady=10)

        gastos_fijos_campos = ["Renta", "Luz", "Internet/Teléfono", "Flota", "Transporte","Limpieza", "Publicidad", "Combustible"]
        gastos_operacionales_campos = ["TSS", "INFOTEP", "Anticipo",]
        gastos_varios_campos = ["Mobiliario", "Consumible/compra",]

        frame_fijos = ttkbcliner.Frame(notebook, padding=10)
        frame_operacionales = ttkbcliner.Frame(notebook, padding=10)
        frame_varios = ttkbcliner.Frame(notebook, padding=10)

        notebook.add(frame_fijos, text="Gastos Fijos")
        notebook.add(frame_operacionales, text="Gastos Operacionales")
        notebook.add(frame_varios, text="Gastos Variados")

        def crear_campos(frame, campos):
            entradas = {}
            for campo in campos:
                fila = ttkbcliner.Frame(frame)
                fila.pack(fill='x', pady=4)
                ttkbcliner.Label(fila, text=campo + ": ", width=20).pack(side='left')
                entrada = ttkbcliner.Entry(fila)
                entrada.pack(side='left', fill='x', expand=True)
                entradas[campo] = entrada
            return entradas

        self.entradas_fijos = crear_campos(frame_fijos, gastos_fijos_campos)
        self.entradas_operacionales = crear_campos(frame_operacionales, gastos_operacionales_campos)
        self.entradas_varios = crear_campos(frame_varios, gastos_varios_campos)

        btn_guardar = ttkbcliner.Button(ventana, text="Guardar Gastos", bootstyle="success", command=self.guardar_gastos_detallados)
        btn_guardar.pack(pady=10)
        

    def guardar_gastos_detallados(self):
        def validar_y_guardar(entradas, categoria_general):
            for campo, entrada in entradas.items():
                valor = entrada.get().strip()
                if valor:
                    try:
                        monto = float(valor)
                        fecha = datetime.now().strftime("%Y-%m-%d")
                        guardar_csv(GASTOS_FILE, [fecha, self.usuario, monto, f"{categoria_general} - {campo}", ""])
                        guardar_en_mysql("Gastos", [fecha, self.usuario, monto, f"{categoria_general} - {campo}", ""])
                    except ValueError:
                        messagebox.showwarning("Valor inválido", f"El valor de '{campo}' no es válido")
                        return False
            return True

        if not validar_y_guardar(self.entradas_fijos, "Gastos Fijos"): return
        if not validar_y_guardar(self.entradas_operacionales, "Gastos Operacionales"): return
        if not validar_y_guardar(self.entradas_varios, "Gastos Variados"): return
        
        messagebox.showinfo("Éxito", "Gastos guardados correctamente")

    def mostrar_registrar_ingreso(self):
        ventana = Toplevel(self.root)
        ventana.title("Registrar Ingreso")
        ventana.geometry("400x400")

        ttkbcliner.Label(ventana, text="Monto del ingreso:", font=("Segoe UI", 12)).pack(pady=8)
        monto_entry = ttkbcliner.Entry(ventana)
        monto_entry.pack(pady=5, fill='x', padx=20)

        ttkbcliner.Label(ventana, text="Fuente del ingreso:", font=("Segoe UI", 12)).pack(pady=8)
        fuente_var = StringVar(value="Transferencia")
        opciones_fuente = ["Transferencia", "Tarjeta", "Efectivo"]
        fuente_menu = ttkbcliner.OptionMenu(ventana, fuente_var, opciones_fuente[0], *opciones_fuente)
        fuente_menu.pack(pady=5, fill='x', padx=20)

        ttkbcliner.Label(ventana, text="Descripción:", font=("Segoe UI", 12)).pack(pady=8)
        descripcion_text = Text(ventana, height=4)
        descripcion_text.pack(pady=5, fill='both', padx=20)

        def guardar_ingresos():
            monto_str = monto_entry.get().strip()
            if not monto_str:
                messagebox.showwarning("Entrada requerida", "Ingrese un monto")
                return
            try:
                monto = float(monto_str)
            except ValueError:
                messagebox.showwarning("Valor inválido", "El monto debe ser un número")
                return
            fuente = fuente_var.get()
            descripcion = descripcion_text.get("1.0", "end").strip()
            fecha = datetime.now().strftime("%Y-%m-%d")
            datos = [fecha, self.usuario, monto, fuente, descripcion]

            guardar_csv(INGRESOS_FILE, [fecha, self.usuario, monto, fuente, descripcion])
            guardar_en_mysql("Ingresos", [fecha, self.usuario, monto, fuente, descripcion])

            messagebox.showinfo("Éxito", "Ingreso registrado exitosamente")
            ventana.destroy()
            print("usuario:", self.usuario)
            
            print("Datos a guardar:", datos)
        ttkbcliner.Button(ventana, text="Guardar Ingresos", bootstyle="success", command=guardar_ingresos).pack(pady=15)


    def mostrar_vista_previa_exportar(self):
        df_gastos = pd.DataFrame(leer_csv(GASTOS_FILE))
        df_ingresos = pd.DataFrame(leer_csv(INGRESOS_FILE))
        if df_gastos.empty and df_ingresos.empty:
            messagebox.showerror("Error", "No hay datos para mostrar")
            return
        VistaPrevia(self.root, df_gastos, df_ingresos, self.exportar_todo_excel)

    def exportar_todo_excel(self):
        exportar_a_excel_consolidado(GASTOS_FILE, INGRESOS_FILE, "datos_consolidados.xlsx", usuario_actual=self.usuario)

    def ver_logs(self):
        if not os.path.exists(LOG_SESIONES):
            messagebox.showerror("Error", "No hay registros de sesiones")
            return
        logs = leer_csv(LOG_SESIONES)
        log_text = "\n".join([" | ".join(row) for row in logs])
        
        # Crear una ventana Toplevel para mostrar los logs
        ventana_logs = Toplevel(self.root)
        ventana_logs.title("Historial de Sesiones")
        ventana_logs.geometry("500x400")
        
        text_area = Text(ventana_logs, wrap="word", font=("Courier New", 10))
        text_area.pack(expand=True, fill="both", padx=10, pady=10)
        text_area.insert("1.0", log_text)
        text_area.config(state="disabled") # Hacer el texto de solo lectura
        
        ttk.Scrollbar(text_area, command=text_area.yview).pack(side="right", fill="y")
        text_area['yscrollcommand'] = ttk.Scrollbar(text_area).set

    def mostrar_menu_exportacion_usuario(self):
        ventana = Toplevel(self.root)
        ventana.title("Crear Informe por Período")
        ventana.geometry("400x220")

        ttkbcliner.Label(ventana, text="Seleccione el período:", font=("Segoe UI", 12)).pack(pady=15)

        periodo_var = StringVar(value="semanal")
        opciones = ["semanal", "mensual"]
        periodo_menu = ttkbcliner.OptionMenu(ventana, periodo_var, opciones[0], *opciones)
        periodo_menu.pack(pady=5)

        def exportar():
            periodo = periodo_var.get()
            self.exportar_reporte_usuario(self.usuario, periodo)
            ventana.destroy()

        ttkbcliner.Button(ventana, text="Exportar Informe", bootstyle="success", command=exportar).pack(pady=20)

    def exportar_reporte_usuario(self, usuario, periodo="semanal"):
        def filtrar_datos_por_periodo(df, periodo):
            if df.empty:
                return df
            
            # Asignar nombres de columna temporales para la manipulación
            temp_cols = [f'col_{i}' for i in range(len(df.columns))]
            df.columns = temp_cols
            
            df[temp_cols[0]] = pd.to_datetime(df[temp_cols[0]], errors='coerce')
            hoy = datetime.now()
            if periodo == "semanal":
                fecha_inicio = hoy - pd.Timedelta(days=hoy.weekday())
            elif periodo == "mensual":
                fecha_inicio = hoy.replace(day=1)
            else:
                return df
            return df[df[temp_cols[0]] >= fecha_inicio]

        df_gastos = pd.DataFrame(leer_csv(GASTOS_FILE))
        df_ingresos = pd.DataFrame(leer_csv(INGRESOS_FILE))

        if not df_gastos.empty:
            df_gastos = df_gastos[df_gastos[1] == usuario]
            df_gastos = filtrar_datos_por_periodo(df_gastos, periodo)

        if not df_ingresos.empty:
            df_ingresos = df_ingresos[df_ingresos[1] == usuario]
            df_ingresos = filtrar_datos_por_periodo(df_ingresos, periodo)

        if df_gastos.empty and df_ingresos.empty:
            messagebox.showinfo("Sin datos", "No hay datos disponibles para exportar en este período.")
            return

        archivo_excel = f"{usuario}_{periodo}_reporte.xlsx"
        exportar_a_excel_consolidado(df_gastos, df_ingresos, archivo_excel, usuario_actual=usuario)

    def exportar_todo_usuario_actual(self):
        df_gastos = pd.DataFrame(leer_csv(GASTOS_FILE))
        df_ingresos = pd.DataFrame(leer_csv(INGRESOS_FILE))

        if not df_gastos.empty:
            df_gastos = df_gastos[df_gastos[1] == self.usuario]
        if not df_ingresos.empty:
            df_ingresos = df_ingresos[df_ingresos[1] == self.usuario]

        if df_gastos.empty and df_ingresos.empty:
            messagebox.showinfo("Sin datos", "No hay datos disponibles para exportar.")
            return

        archivo_excel = f"{self.usuario}_exportacion_completa.xlsx"
        exportar_a_excel_consolidado(df_gastos, df_ingresos, archivo_excel, usuario_actual=self.usuario)
    
    # --- GESTIÓN DE EMPRESAS (CORREGIDO) ---
    def gestion_empresas(self):
        """Muestra una ventana para seleccionar una empresa y editar sus gastos."""
        ventana = Toplevel(self.root)
        ventana.title("Gestión de Empresas")
        ventana.geometry("400x300")

        ttkbcliner.Label(ventana, text="🏢 Selección de Empresa", font=("Segoe UI", 14, "bold")).pack(pady=10)

        lista_empresas = list(usuarios.keys()) 

        for empresa in lista_empresas:
            btn = ttkbcliner.Button(ventana, text=empresa, command=lambda e=empresa: self.mostrar_formulario_gastos_empresa(e))
            btn.pack(pady=5, padx=20, fill='x')

    def mostrar_formulario_gastos_empresa(self, empresa):
        """Muestra un formulario para registrar gastos fijos de una empresa específica."""
        ventana_form = Toplevel(self.root)
        ventana_form.title(f"Formulario de Gastos para {empresa}")
        ventana_form.geometry("450x350")

        ttkbcliner.Label(ventana_form, text=f"✏️ Gastos Fijos para {empresa}", font=("Segoe UI", 12, "bold")).pack(pady=10)

        frame_campos = ttkbcliner.Frame(ventana_form, padding=10)
        frame_campos.pack(expand=True, fill='both')

        entradas = {}
        campos_gastos = ["Nómina", "Comisiones", "Dietas", "Bonos","Descuentos",]

        for campo in campos_gastos:
            fila = ttkbcliner.Frame(frame_campos)
            fila.pack(fill='x', pady=5)
            ttkbcliner.Label(fila, text=f"{campo}:", width=20).pack(side='left')
            entry = ttkbcliner.Entry(fila)
            entry.pack(side='left', fill='x', expand=True)
            entradas[campo] = entry

        def accion_guardar():
            self.guardar_gastos_empresa(empresa, entradas)
            ventana_form.destroy()

        btn_guardar = ttkbcliner.Button(ventana_form, text="Guardar Gastos", bootstyle="success", command=accion_guardar)
        btn_guardar.pack(pady=15)
        

    def guardar_gastos_empresa(self, empresa, entradas):
        """Valida y guarda los gastos introducidos en el formulario."""
        fecha = datetime.now().strftime("%Y-%m-%d")
        
        for nombre_campo, entry_widget in entradas.items():
            monto_str = entry_widget.get().strip()
            if monto_str:
                try:
                    monto = float(monto_str)
                    guardar_csv(GASTOS_FILE, [fecha, empresa, monto, f"Gastos Fijos - {nombre_campo}", "Formulario de Admin"])
                    guardar_en_mysql("Gastos", [fecha, empresa, monto, f"Gastos Fijos - {nombre_campo}", "Formulario de Admin"])

                except ValueError:
                    messagebox.showwarning("Valor Inválido", f"El valor para '{nombre_campo}' no es un número válido y será omitido.")
                    continue
        
        messagebox.showinfo("Éxito", f"Gastos para {empresa} guardados correctamente.")

        # --- Ejecutar ---
if __name__ == "__main__":
    app = ttkbcliner.Window(themename="morph")
    SistemaFinancieroApp(app)
    app.mainloop()


        # --- separador ---

        # Aquí puedes agregar cualquier lógica adicional que necesites

        # --- Ejecutar ---
def guardar_en_mysql(tabla, datos):
    """
    Inserta datos en MySQL (Railway).
    tabla: 'ingresos' o 'gastos'
    datos: lista [fecha, usuario, monto, categoria, descripcion]
    """
    try:
        conexion = mysql.connector.connect(
            host="yamanote.proxy.rlwy.net",
            port=18234,
            database="Railway",
            user="root",
            password="UyuZkiAaxFytvlevPCSrGMNPKhOeYxXT",
            #ssl_ca="ca.pem"   # ⚠️ Debes descargar este archivo desde Aiven
        )
        cursor = conexion.cursor()

        if tabla.lower() == "ingresos":
            query = """INSERT INTO ingresos (fecha, usuario, monto, categoria, descripcion)
                       VALUES (%s, %s, %s, %s, %s)"""
        elif tabla.lower() == "gastos":
            query = """INSERT INTO Gastos (fecha, usuario, monto, categoria, descripcion)
                       VALUES (%s, %s, %s, %s, %s)"""
        else:
            raise ValueError("Tabla no válida")

        cursor.execute(query, tuple(datos))
        conexion.commit()
        cursor.close()
        conexion.close()

    except mysql.connector.Error as e:
        print(f"❌ Error MySQL: {e}")


# --- Utilidades de archivo ---
def guardar_csv(archivo, datos):
    with open(archivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(datos)

...
# (aquí sigue todo tu código igual hasta las funciones que guardan datos)
...

def guardar_gastos_detallados(self):
        def validar_y_guardar(entradas, categoria_general):
            for campo, entrada in entradas.items():
                valor = entrada.get().strip()
                if valor:
                    try:
                        monto = float(valor)
                        fecha = datetime.now().strftime("%Y-%m-%d")
                        datos = [fecha, self.usuario, monto, f"{categoria_general} - {campo}", ""]
                        
                        guardar_csv(GASTOS_FILE, datos)              # Guardar en CSV
                        guardar_en_mysql("Gastos", datos)            # Guardar en MySQL

                    except ValueError:
                        messagebox.showwarning("Valor inválido", f"El valor de '{campo}' no es válido")
                        return False
            return True

        if not validar_y_guardar(self.entradas_fijos, "Gastos Fijos"): return
        if not validar_y_guardar(self.entradas_operacionales, "Gastos Operacionales"): return
        if not validar_y_guardar(self.entradas_varios, "Gastos Variados"): return
        
        messagebox.showinfo("Éxito", "Gastos guardados correctamente")

def mostrar_registrar_ingreso(self):
        ventana = Toplevel(self.root)
        ventana.title("Registrar Ingresos")
        ventana.geometry("400x400")
        usuario_actual = self.usuario  # Guardar el usuario actual en una variable local

        ttkbcliner.Label(ventana, text="Monto del ingreso:", font=("Segoe UI", 12)).pack(pady=8)
        monto_entry = ttkbcliner.Entry(ventana)
        monto_entry.pack(pady=5, fill='x', padx=20)

        ttkbcliner.Label(ventana, text="Fuente del ingreso:", font=("Segoe UI", 12)).pack(pady=8)
        fuente_var = StringVar(value="Transferencia")
        opciones_fuente = ["Transferencia", "Tarjeta", "Efectivo"]
        fuente_menu = ttkbcliner.OptionMenu(ventana, fuente_var, opciones_fuente[0], *opciones_fuente)
        fuente_menu.pack(pady=5, fill='x', padx=20)

        ttkbcliner.Label(ventana, text="Descripción:", font=("Segoe UI", 12)).pack(pady=8)
        descripcion_text = Text(ventana, height=4)
        descripcion_text.pack(pady=5, fill='both', padx=20)

        def guardar_ingreso()-> None: # type: ignore
            print("Ingreso guardado correctamente.")
            #llama la funcion 
            guardar_ingreso()
            monto_str = monto_entry.get().strip()
            if not monto_str:
                messagebox.showwarning("Entrada requerida", "Ingrese un monto")
                return
            try:
                monto = float(monto_str)
                # Eliminar la línea que usa 'empresa' y 'nombre_campo' porque no existen aquí

            except ValueError:
                messagebox.showwarning("Valor inválido", "El monto debe ser un número")
                return
            fuente = fuente_var.get()
            descripcion = descripcion_text.get("1.0", "end").strip()
            fecha = datetime.now().strftime("%Y-%m-%d")
            
            datos = [fecha, self.usuario, monto, fuente, descripcion]
            guardar_csv(INGRESOS_FILE, datos)           # Guardar en CSV
            guardar_en_mysql("Ingresos", datos)         # Guardar en MySQL
            print("usuario:", self.usuario)
            print("Datos a guardar:", datos)

            messagebox.showinfo("Éxito", "Ingreso registrado exitosamente")
            ventana.destroy()

        ttkbcliner.Button(ventana, text="Guardar Ingreso", bootstyle="success", command=self.guardar_ingreso).pack(pady=15)


def guardar_gastos_empresa(self, empresa, entradas):
        """Valida y guarda los gastos introducidos en el formulario."""
        fecha = datetime.now().strftime("%Y-%m-%d")
        
        for nombre_campo, entry_widget in entradas.items():
            monto_str = entry_widget.get().strip()
            if monto_str:
                try:
                    monto = float(monto_str)
                    datos = [fecha, empresa, monto, f"Gastos Fijos - {nombre_campo}", "Formulario de Admin"]
                    
                    guardar_csv(GASTOS_FILE, datos)         # Guardar en CSV
                    guardar_en_mysql("Gastos", datos)       # Guardar en MySQL
                    

                except ValueError:
                    messagebox.showwarning("Valor Inválido", f"El valor para '{nombre_campo}' no es un número válido y será omitido.")
                    continue
        
        messagebox.showinfo("Éxito", f"Gastos para {empresa} guardados correctamente.")


def guardar_ingreso_empresa(self, empresa,entradas):
        """Valida y guarda los ingresos introducidos en el formulario."""
        fecha = datetime.now().strftime("%Y-%m-%d")
        
        for nombre_campo, entry_widget in entradas.items():
            monto_str = entry_widget.get().strip()
            if monto_str:
                try:
                    monto = float(monto_str)
                    datos = [fecha, empresa, monto, f"Ingresos - {nombre_campo}", "Formulario de Admin"]
                    
                    guardar_csv(INGRESOS_FILE, datos)         # Guardar en CSV
                    guardar_en_mysql("Ingresos", datos)       # Guardar en MySQL
                    

                except ValueError:
                    messagebox.showwarning("Valor Inválido", f"El valor para '{nombre_campo}' no es un número válido y será omitido.")
                    continue
        
        messagebox.showinfo("Éxito", f"Ingresos para {empresa} guardados correctamente.")