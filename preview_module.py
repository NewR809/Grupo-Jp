import tkinter as tk
from tkinter import ttk, messagebox

class VistaPrevia(tk.Toplevel):
    def __init__(self, master, columns, data, on_save, validation_func=None, title="Vista previa"):
        super().__init__(master)
        self.title(title)
        self.geometry("900x500")
        self.columns = columns
        self.validation_func = validation_func
        self.on_save = on_save

        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", height=14)
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="w")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        for row in data:
            self.tree.insert("", "end", values=row)

        btns = ttk.Frame(self)
        btns.pack(pady=10)
        ttk.Button(btns, text="✏️ Editar fila", command=self._editar_fila).pack(side="left", padx=8)
        ttk.Button(btns, text="➕ Agregar fila", command=self._agregar_fila).pack(side="left", padx=8)
        ttk.Button(btns, text="🗑️ Eliminar fila", command=self._eliminar_fila).pack(side="left", padx=8)
        ttk.Button(btns, text="✅ Confirmar y guardar", command=self._confirmar).pack(side="left", padx=8)
        ttk.Button(btns, text="❌ Cancelar", command=self.destroy).pack(side="left", padx=8)

    def _get_all_rows(self):
        return [list(self.tree.item(iid, "values")) for iid in self.tree.get_children()]

    def _editar_fila(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona una fila")
            return
        iid = sel[0]
        valores = list(self.tree.item(iid, "values"))

        win = tk.Toplevel(self)
        win.title("Editar fila")
        win.geometry("420x400")
        entries = []
        for i, col in enumerate(self.columns):
            ttk.Label(win, text=col + ":").pack(pady=5, anchor="w")
            e = ttk.Entry(win)
            e.insert(0, valores[i])
            e.pack(fill="x", padx=14)
            entries.append(e)

        def guardar():
            nuevos = [e.get().strip() for e in entries]
            self.tree.item(iid, values=nuevos)
            win.destroy()

        ttk.Button(win, text="Guardar cambios", command=guardar).pack(pady=14)

    def _agregar_fila(self):
        self.tree.insert("", "end", values=["" for _ in self.columns])

    def _eliminar_fila(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona una fila")
            return
        self.tree.delete(sel[0])

    def _confirmar(self):
        dataset = self._get_all_rows()
        dataset = [row for row in dataset if any(str(x).strip() for x in row)]
        if not dataset:
            messagebox.showwarning("Sin datos", "No hay filas válidas para guardar")
            return
        if self.validation_func:
            valid = self.validation_func(dataset)
            if valid is not True:
                messagebox.showwarning("Validación", valid)
                return
        try:
            self.on_save(dataset)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))