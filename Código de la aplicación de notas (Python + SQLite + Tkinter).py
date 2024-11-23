import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def conectar_db():
    conn = sqlite3.connect('notas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notas
                 (id INTEGER PRIMARY KEY, titulo TEXT, contenido TEXT)''')
    conn.commit()
    return conn

def agregar_nota(titulo, contenido):
    conn = conectar_db()
    c = conn.cursor()
    c.execute('INSERT INTO notas (titulo, contenido) VALUES (?, ?)', (titulo, contenido))
    conn.commit()
    conn.close()

def mostrar_notas():
    conn = conectar_db()
    c = conn.cursor()
    c.execute('SELECT * FROM notas')
    notas = c.fetchall()
    conn.close()
    return notas

def editar_nota(id_nota, nuevo_titulo, nuevo_contenido):
    conn = conectar_db()
    c = conn.cursor()
    c.execute('UPDATE notas SET titulo = ?, contenido = ? WHERE id = ?', (nuevo_titulo, nuevo_contenido, id_nota))
    conn.commit()
    conn.close()

def eliminar_nota(id_nota):
    conn = conectar_db()
    c = conn.cursor()
    c.execute('DELETE FROM notas WHERE id = ?', (id_nota,))
    conn.commit()
    conn.close()

def buscar_nota(titulo):
    conn = conectar_db()
    c = conn.cursor()
    c.execute('SELECT * FROM notas WHERE titulo LIKE ?', ('%' + titulo + '%',))
    notas = c.fetchall()
    conn.close()
    return notas

def ventana_principal():
    root = tk.Tk()
    root.title("Aplicación de Notas")
    root.geometry("500x500")
    root.configure(bg="#f7f7f7")

    title_font = ('Arial', 18, 'bold')
    button_font = ('Arial', 12)

    tk.Label(root, text="Mi Aplicación de Notas", font=title_font, bg="#f7f7f7", fg="#333").pack(pady=30)

    crear_boton(root, "Agregar Nota", agregar_ventana, "#007bff", "#0056b3").pack(pady=10, fill="x", padx=50)
    crear_boton(root, "Mostrar Notas", mostrar_ventana, "#28a745", "#1e7e34").pack(pady=10, fill="x", padx=50)
    crear_boton(root, "Buscar Nota", buscar_ventana, "#ffc107", "#e0a800").pack(pady=10, fill="x", padx=50)

    root.mainloop()

def crear_boton(master, texto, comando, color1, color2):
    boton = tk.Button(master, text=texto, command=comando, font=('Arial', 12), bg=color1, fg="white", relief="flat", padx=20, pady=10)
    boton.bind("<Enter>", lambda event, b=boton: b.config(bg=color2))
    boton.bind("<Leave>", lambda event, b=boton: b.config(bg=color1))
    return boton

def agregar_ventana():
    def guardar_nota():
        titulo = entry_titulo.get()
        contenido = entry_contenido.get()
        if titulo and contenido:
            agregar_nota(titulo, contenido)
            messagebox.showinfo("Éxito", "Nota agregada correctamente")
            ventana_agregar.destroy()
        else:
            messagebox.showwarning("Error", "Por favor, ingrese un título y contenido")

    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Nota")
    ventana_agregar.geometry("400x300")
    ventana_agregar.configure(bg="#f7f7f7")

    tk.Label(ventana_agregar, text="Título:", bg="#f7f7f7", font=('Arial', 12)).pack(pady=10)
    entry_titulo = tk.Entry(ventana_agregar, font=('Arial', 12), bd=2, relief="solid")
    entry_titulo.pack(pady=5, padx=10, fill="x")

    tk.Label(ventana_agregar, text="Contenido:", bg="#f7f7f7", font=('Arial', 12)).pack(pady=10)
    entry_contenido = tk.Entry(ventana_agregar, font=('Arial', 12), bd=2, relief="solid")
    entry_contenido.pack(pady=5, padx=10, fill="x")

    crear_boton(ventana_agregar, "Guardar Nota", guardar_nota, "#007bff", "#0056b3").pack(pady=20)

def mostrar_ventana():
    notas = mostrar_notas()

    ventana_mostrar = tk.Toplevel()
    ventana_mostrar.title("Mostrar Notas")
    ventana_mostrar.geometry("500x400")
    ventana_mostrar.configure(bg="#f7f7f7")

    for nota in notas:
        tk.Label(ventana_mostrar, text=f"Título: {nota[1]}\nContenido: {nota[2]}", bg="#f7f7f7", font=('Arial', 12), anchor="w").pack(pady=10, padx=20, fill="x")

def buscar_ventana():
    def buscar():
        titulo = entry_buscar.get()
        notas = buscar_nota(titulo)
        ventana_resultados = tk.Toplevel()
        ventana_resultados.title("Resultados de la Búsqueda")
        ventana_resultados.geometry("500x400")
        ventana_resultados.configure(bg="#f7f7f7")

        if notas:
            for nota in notas:
                tk.Label(ventana_resultados, text=f"Título: {nota[1]}\nContenido: {nota[2]}", bg="#f7f7f7", font=('Arial', 12), anchor="w").pack(pady=10, padx=20, fill="x")
        else:
            tk.Label(ventana_resultados, text="No se encontraron resultados", bg="#f7f7f7", font=('Arial', 12), anchor="w").pack(pady=10, padx=20)

    ventana_buscar = tk.Toplevel()
    ventana_buscar.title("Buscar Nota")
    ventana_buscar.geometry("400x200")
    ventana_buscar.configure(bg="#f7f7f7")

    tk.Label(ventana_buscar, text="Ingrese el título de la nota:", bg="#f7f7f7", font=('Arial', 12)).pack(pady=10)
    entry_buscar = tk.Entry(ventana_buscar, font=('Arial', 12), bd=2, relief="solid")
    entry_buscar.pack(pady=5, padx=10, fill="x")

    crear_boton(ventana_buscar, "Buscar", buscar, "#28a745", "#1e7e34").pack(pady=20)

if __name__ == "__main__":
    ventana_principal()
