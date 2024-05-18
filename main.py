import tkinter as tk
from tkinter import messagebox

class Coleador:
    def __init__(self, nombre, estado, puntos_nulos, puntos_efectivos):
        self.posicion = 0
        self.nombre = nombre
        self.estado = estado
        self.puntos_nulos = int(puntos_nulos)
        self.puntos_efectivos = int(puntos_efectivos)

    def __str__(self):
        return self.nombre

    def puntuacion(self):
        return self.puntos_efectivos - self.puntos_nulos

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Coleadores")

        self.lista_coleadores = []

        self.create_widgets()
        self.load_coleadores()

    def create_widgets(self):
        tk.Label(self.root, text="Nombre:").grid(row=0, column=0)
        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(self.root, text="Estado:").grid(row=1, column=0)
        self.entry_estado = tk.Entry(self.root)
        self.entry_estado.grid(row=1, column=1)

        tk.Label(self.root, text="Puntos Nulos:").grid(row=2, column=0)
        self.entry_puntos_nulos = tk.Entry(self.root)
        self.entry_puntos_nulos.grid(row=2, column=1)

        tk.Label(self.root, text="Puntos Efectivos:").grid(row=3, column=0)
        self.entry_puntos_efectivos = tk.Entry(self.root)
        self.entry_puntos_efectivos.grid(row=3, column=1)

        self.listbox = tk.Listbox(self.root)
        self.listbox.grid(row=0, column=2, rowspan=6)
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        self.listbox.bind('<Button-1>', self.start_drag)
        self.listbox.bind('<B1-Motion>', self.on_drag)
        self.listbox.bind('<ButtonRelease-1>', self.stop_drag)

        self.drag_data = {"index": None}

        self.listbox_sorted = tk.Listbox(self.root)
        self.listbox_sorted.grid(row=0, column=3, rowspan=6)

        tk.Button(self.root, text="Agregar", command=self.add_coleador).grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Modificar", command=self.update_coleador).grid(row=5, column=0, columnspan=2)
        tk.Button(self.root, text="Eliminar", command=self.delete_coleador).grid(row=6, column=0, columnspan=2)

        # Adding labels and listboxes for "Turno Actual" and "Turno Siguiente"
        tk.Label(self.root, text="Turno Actual:").grid(row=7, column=0, columnspan=2)
        self.listbox_turno_actual = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.listbox_turno_actual.grid(row=8, column=0, columnspan=2)

        tk.Label(self.root, text="Turno Siguiente:").grid(row=9, column=0, columnspan=2)
        self.listbox_turno_siguiente = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.listbox_turno_siguiente.grid(row=10, column=0, columnspan=2)

        tk.Button(self.root, text="Agregar a Turno Actual", command=self.agregar_actual).grid(row=11, column=0, columnspan=2)
        tk.Button(self.root, text="Agregar a Turno Siguiente", command=self.agregar_siguiente).grid(row=12, column=0, columnspan=2)
        tk.Button(self.root, text="Siguiente Turno", command=self.siguiente_turno).grid(row=13, column=0, columnspan=2)

    def start_drag(self, event):
        widget = event.widget
        self.drag_data["index"] = widget.nearest(event.y)

    def on_drag(self, event):
        widget = event.widget
        index = widget.nearest(event.y)

        if index != self.drag_data["index"]:
            self.listbox.delete(self.drag_data["index"])
            self.listbox.insert(index, self.lista_coleadores[self.drag_data["index"]].nombre)
            self.lista_coleadores.insert(index, self.lista_coleadores.pop(self.drag_data["index"]))
            self.drag_data["index"] = index

    def stop_drag(self, event):
        self.save_coleadores()
        self.update_sorted_listbox()

    def add_coleador(self):
        nombre = self.entry_nombre.get()
        estado = self.entry_estado.get()
        puntos_nulos = self.entry_puntos_nulos.get()
        puntos_efectivos = self.entry_puntos_efectivos.get()

        if nombre and estado and puntos_nulos and puntos_efectivos:
            coleador = Coleador(nombre, estado, puntos_nulos, puntos_efectivos)
            self.lista_coleadores.append(coleador)
            self.update_listbox()
            self.update_sorted_listbox()
            self.save_coleadores()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son requeridos")

    def update_coleador(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Advertencia", "Seleccione un coleador para modificar")
            return
        
        nombre = self.entry_nombre.get()
        estado = self.entry_estado.get()
        puntos_nulos = self.entry_puntos_nulos.get()
        puntos_efectivos = self.entry_puntos_efectivos.get()

        if nombre and estado and puntos_nulos and puntos_efectivos:
            index = selected_index[0]
            coleador = self.lista_coleadores[index]
            coleador.nombre = nombre
            coleador.estado = estado
            coleador.puntos_nulos = int(puntos_nulos)
            coleador.puntos_efectivos = int(puntos_efectivos)
            self.update_listbox()
            self.update_sorted_listbox()
            self.save_coleadores()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son requeridos")

    def delete_coleador(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Advertencia", "Seleccione un coleador para eliminar")
            return

        index = selected_index[0]
        del self.lista_coleadores[index]
        self.update_listbox()
        self.update_sorted_listbox()
        self.save_coleadores()

    def on_listbox_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            coleador = self.lista_coleadores[index]
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, coleador.nombre)
            self.entry_estado.delete(0, tk.END)
            self.entry_estado.insert(0, coleador.estado)
            self.entry_puntos_nulos.delete(0, tk.END)
            self.entry_puntos_nulos.insert(0, coleador.puntos_nulos)
            self.entry_puntos_efectivos.delete(0, tk.END)
            self.entry_puntos_efectivos.insert(0, coleador.puntos_efectivos)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for coleador in self.lista_coleadores:
            self.listbox.insert(tk.END, coleador.nombre)
        self.save_coleadores()

    def update_sorted_listbox(self):
        sorted_coleadores = sorted(self.lista_coleadores, key=lambda c: c.puntuacion(), reverse=True)
        self.listbox_sorted.delete(0, tk.END)
        for coleador in sorted_coleadores:
            self.listbox_sorted.insert(tk.END, coleador.nombre)
        self.save_sorted_coleadores()

    def save_sorted_coleadores(self):
        with open("lista_posiciones.txt", "w") as file:
            for index in range(self.listbox_sorted.size()):
                file.write(f"{self.listbox_sorted.get(index)}\n")

    def save_coleadores(self):
        with open("coleadores.txt", "w") as file:
            for coleador in self.lista_coleadores:
                file.write(f"{coleador.nombre},{coleador.estado},{coleador.puntos_nulos},{coleador.puntos_efectivos}\n")

    def load_coleadores(self):
        try:
            with open("coleadores.txt", "r") as file:
                for line in file:
                    nombre, estado, puntos_nulos, puntos_efectivos = line.strip().split(',')
                    coleador = Coleador(nombre, estado, puntos_nulos, puntos_efectivos)
                    self.lista_coleadores.append(coleador)
            self.update_listbox()
            self.update_sorted_listbox()
        except FileNotFoundError:
            pass

    def agregar_actual(self):
        selected_indices = self.listbox.curselection()
        if len(self.listbox_turno_actual.get(0, tk.END)) + len(selected_indices) <= 4:
            for i in selected_indices:
                coleador_nombre = self.listbox.get(i)
                if coleador_nombre not in self.listbox_turno_actual.get(0, tk.END):
                    self.listbox_turno_actual.insert(tk.END, coleador_nombre)
        else:
            messagebox.showwarning("Advertencia", "Máximo 4 coleadores en el turno actual")

    def agregar_siguiente(self):
        selected_indices = self.listbox.curselection()
        if len(self.listbox_turno_siguiente.get(0, tk.END)) + len(selected_indices) <= 4:
            for i in selected_indices:
                coleador_nombre = self.listbox.get(i)
                if coleador_nombre not in self.listbox_turno_siguiente.get(0, tk.END):
                    self.listbox_turno_siguiente.insert(tk.END, coleador_nombre)
        else:
            messagebox.showwarning("Advertencia", "Máximo 4 coleadores en el turno siguiente")

    def siguiente_turno(self):
        self.listbox_turno_actual.delete(0, tk.END)
        for i in range(self.listbox_turno_siguiente.size()):
            self.listbox_turno_actual.insert(tk.END, self.listbox_turno_siguiente.get(i))
        self.listbox_turno_siguiente.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
