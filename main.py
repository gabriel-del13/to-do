
"""
from tkinter import Tk, Label
from PIL import Image, ImageTk
import tkinter as tk

window = tk.Tk()
window.geometry("700x400")
window.resizable(False, False)

background= Image.open('zero_two.jpg')
background = background.resize((700, 400), Image.LANCZOS)
background_tk = ImageTk.PhotoImage(background)

background_label = Label(window, image=background_tk)
background_label.place (x=0, y=0, relwidth = 1, relheight=1)
window.mainloop()

"""

# todo esto fue basicamente con chat gpt pero, nos podemos hacer una idea con esto
import tkinter as tk  # Importamos Tkinter
from PIL import Image, ImageTk  # importamos el pillow


# Crear la ventana principal
root = tk.Tk()
root.title("Gestor de Tareas")  # Título de la ventana
root.geometry("400x600")  # Tamaño de la ventana (ancho x alto)
root.config(bg="white")  # Color de fondo de la ventana

# Crear un marco (Frame) para contener los elementos de la UI
frame = tk.Frame(root)
frame.pack(pady=20)

# Listbox para mostrar las tareas
listbox = tk.Listbox(
    frame,
    width=40,
    height=10,
    bg="White",
    font=("Arial", 12),
    selectbackground="gray",
    activestyle="none"
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Scrollbar para el Listbox
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Entry widget para agregar nuevas tareas
entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=20)

# Botón para agregar una nueva tarea
add_task_button = tk.Button(
    root, text="Agregar Tarea", width=20, command=lambda: agregar_tarea())
add_task_button.pack(pady=10)

# Botón para eliminar una tarea seleccionada
delete_task_button = tk.Button(
    root, text="Eliminar Tarea", width=20, command=lambda: eliminar_tarea())
delete_task_button.pack(pady=10)

# Botón para marcar una tarea como completada
mark_task_button = tk.Button(
    root, text="Marcar como Completa", width=20, command=lambda: marcar_completada())
mark_task_button.pack(pady=10)


def agregar_tarea():
    tarea = entry.get()
    if tarea != "":
        listbox.insert(tk.END, tarea)
        entry.delete(0, tk.END)
    else:
        print("El campo de tarea está vacío.")


def eliminar_tarea():
    try:
        tarea_seleccionada = listbox.curselection()[0]
        listbox.delete(tarea_seleccionada)
    except:
        print("No hay tarea seleccionada.")


def marcar_completada():
    try:
        tarea_seleccionada = listbox.curselection()[0]
        tarea = listbox.get(tarea_seleccionada)
        listbox.delete(tarea_seleccionada)
        listbox.insert(tk.END, f"{tarea} ✔")
    except:
        print("No hay tarea seleccionada.")


# Cargar y configurar la imagen de fondo
bg_image = Image.open("zero_two.jpg")
bg_image = bg_image.resize((400, 600), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Traer los widgets al frente del fondo
frame.lift()
entry.lift()
add_task_button.lift()
delete_task_button.lift()
mark_task_button.lift()

root.mainloop()
