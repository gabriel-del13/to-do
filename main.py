import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()
root.title("Gestor de Tareas")
root.geometry("700x400")
root.config(bg="white")
root.resizable(False, False)

# Cargar y configurar la imagen de fondo
root.iconbitmap('icon.ico')

bg_image = Image.open("zero_two.jpg")
bg_image = bg_image.resize((700, 400), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Crear un marco (Frame) para contener los elementos de la UI
frame = tk.Frame(root, bg="white")
frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=10, anchor='nw')

# Listbox para mostrar las tareas
listbox = tk.Listbox(
    frame,
    width=40,
    height=20,
    bg="White",
    font=("Arial", 12),
    selectbackground="gray",
    activestyle="none"
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, anchor='w')

# Scrollbar para el Listbox
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Crear un marco (Frame) para el campo de entrada
entry_frame = tk.Frame(root, bg="white")
entry_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10, anchor='n')

# Entry widget para agregar nuevas tareas sin placeholder
entry = tk.Entry(entry_frame, width=40, font=("Arial", 12))
entry.pack(pady=10, anchor='center')

# Crear un marco (Frame) para los botones
bottom_frame = tk.Frame(root, bg="white")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10, anchor='se')

# Botón para agregar una nueva tarea
add_task_button = tk.Button(
    bottom_frame, text="Agregar Tarea", width=20, command=lambda: agregar_tarea())
add_task_button.pack(pady=5, anchor='center')

# Botón para eliminar una tarea seleccionada
delete_task_button = tk.Button(
    bottom_frame, text="Eliminar Tarea", width=20, command=lambda: eliminar_tarea())
delete_task_button.pack(pady=5, anchor='center')

# Botón para marcar una tarea como completada
mark_task_button = tk.Button(
    bottom_frame, text="Marcar como Completa", width=20, command=lambda: marcar_completada())
mark_task_button.pack(pady=5, anchor='center')


def agregar_tarea():
    tarea = entry.get()
    if tarea != "":
        listbox.insert(tk.END, tarea)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "El campo de tarea está vacío.")


def eliminar_tarea():
    try:
        tarea_seleccionada = listbox.curselection()[0]
        listbox.delete(tarea_seleccionada)
    except IndexError:
        messagebox.showwarning("Advertencia", "No hay tarea seleccionada.")


def marcar_completada():
    try:
        tarea_seleccionada = listbox.curselection()[0]
        tarea = listbox.get(tarea_seleccionada)
        listbox.delete(tarea_seleccionada)
        listbox.insert(tk.END, f"{tarea} ✔")
    except IndexError:
        messagebox.showwarning("Advertencia", "No hay tarea seleccionada.")


# Traer los widgets al frente del fondo
frame.lift()
entry_frame.lift()
bottom_frame.lift()

root.mainloop()
