import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from desktop.utils import guardar_csv, guardar_en_mysql

class VistaPreviaEditable(tk.Toplevel):
    def __init__(self, master, datos, columnas, tipo, confirm_callback=None):
        super().__init__(master)
        self.title("Vista Previa Editable")
        self.geometry("900x500")
        self.tipo = tipo
        self.columnas = columnas
        self.datos = datos
        self.confirm_callback = confirm_callback
        self.df = pd.DataFrame(datos, columns=columnas)
        self.tree = None

        self.crear_tabla()
        self.crear_botones()

    def crear_tabla(self):
        self.tree = ttk.Treeview(self, columns=self.columnas, show="headings")
        for col in self.columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        for row in self.df.values:
            self.tree.insert("", "end", values=list(row))

    def crear_botones(self):
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        ttk.Button(frame, text="✏️ Editar seleccionado", command=self.editar_registro).pack(side="left", padx=10)
        ttk.Button(frame, text="✅ Confirmar y guardar", command=self.confirmar_guardado).pack(side="left", padx=10)
        ttk.Button(frame, text="❌ Cancelar", command=self.destroy).pack(side="left", padx=10)

    def editar_registro(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sin selección", "Seleccione un registro para editar")
            return

        valores = self.tree.item(selected[0])["values"]
        ventana = tk.Toplevel(self)
        ventana.title("Editar Registro")
        ventana.geometry("400x400")

        entradas = []
        for i, campo in enumerate(self.columnas):
            ttk.Label(ventana, text=campo + ":").pack(pady=5)
            entrada = ttk.Entry(ventana)
            entrada.insert(0, valores[i])
            entrada.pack(fill="x", padx=20)
            entradas.append(entrada)

        def guardar_edicion():
            nuevos_valores = [e.get().strip() for e in entradas]
            self.tree.item(selected[0], values=nuevos_valores)
            index = self.df[(self.df[self.columnas[0]] == valores[0]) & (self.df[self.columnas[1]] == valores[1])].index
            if not index.empty:
                self.df.loc[index[0]] = nuevos_valores
            messagebox.showinfo("Actualizado", "Registro editado correctamente")
            ventana.destroy()

        ttk.Button(ventana, text="Guardar cambios", command=guardar_edicion).pack(pady=20)

    def confirmar_guardado(self):
        for row in self.df.values:
            guardar_csv(f"{self.tipo.lower()}.csv", list(row))
            guardar_en_mysql(self.tipo, list(row))
        if self.confirm_callback:
            self.confirm_callback()
        self.destroy()