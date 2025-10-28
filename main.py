import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import math

class EpicTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        # Colores épicos con gradiente
        self.bg_gradient_start = "#0f0c29"
        self.bg_gradient_mid = "#302b63"
        self.bg_gradient_end = "#24243e"
        self.glass_bg = "#1a1a2e"
        self.accent_color = "#ff1493"
        self.accent_hover = "#ff69b4"
        self.text_color = "#ffffff"
        self.secondary_text = "#ffb6d9"
        
        # Variables de animación
        self.hover_scale = 1.0
        self.particles = []
        
        # Crear canvas de fondo con imagen
        self.canvas = tk.Canvas(root, width=900, height=650, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Cargar y configurar la imagen de fondo
        try:
            bg_image = Image.open("zero_two.jpg")
            bg_image = bg_image.resize((900, 650), Image.Resampling.LANCZOS)
            
            # Aplicar desenfoque y oscurecimiento para efecto épico
            bg_image = bg_image.filter(ImageFilter.GaussianBlur(3))
            enhancer = Image.new('RGBA', bg_image.size, (0, 0, 0, 100))
            bg_image = bg_image.convert('RGBA')
            bg_image = Image.alpha_composite(bg_image, enhancer)
            
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
        except:
            # Si no se encuentra la imagen, usar gradiente
            self.draw_gradient_background()
        
        # Agregar partículas flotantes
        self.create_particles()
        
        # Contenedor principal con efecto glass (semi-transparente)
        self.main_container = tk.Frame(self.canvas, bg=self.glass_bg)
        self.main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=550)
        
        # Crear efecto de cristal con opacidad
        overlay = tk.Frame(self.main_container, bg="#1a1a2e")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        overlay.lower()
        
        # Título épico
        title_frame = tk.Frame(self.main_container, bg=self.glass_bg)
        title_frame.pack(pady=20)
        
        title = tk.Label(
            title_frame,
            text="Gestror de tarea",
            font=("Segoe UI", 28, "bold"),
            fg=self.accent_color,
            bg=self.glass_bg
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Crear, gestionar y conquistar tus tareas diarias",
            font=("Segoe UI", 11),
            fg=self.secondary_text,
            bg=self.glass_bg
        )
        subtitle.pack()
        
        # Contenedor de entrada
        input_container = tk.Frame(self.main_container, bg=self.glass_bg)
        input_container.pack(pady=15, padx=40, fill=tk.X)
        
        # Entry con estilo moderno
        entry_frame = tk.Frame(input_container, bg="#2d2d44", highlightthickness=2, 
                              highlightbackground=self.accent_color, highlightcolor=self.accent_hover)
        entry_frame.pack(fill=tk.X)
        
        self.entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 14),
            bg="#2d2d44",
            fg=self.text_color,
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            bd=0
        )
        self.entry.pack(ipady=12, ipadx=15, fill=tk.X)
        self.entry.insert(0, "Escribe una nueva tarea...")
        self.entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.entry.bind("<Return>", lambda e: self.agregar_tarea())
        
        # Contenedor de la lista
        list_container = tk.Frame(self.main_container, bg=self.glass_bg)
        list_container.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)
        
        # Frame para el listbox con borde
        listbox_frame = tk.Frame(list_container, bg="#2d2d44", highlightthickness=2,
                                highlightbackground="#404060")
        listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Listbox personalizado
        self.listbox = tk.Listbox(
            listbox_frame,
            font=("Segoe UI", 12),
            bg="#2d2d44",
            fg=self.text_color,
            selectbackground=self.accent_color,
            selectforeground="#000000",
            activestyle="none",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Scrollbar personalizado
        scrollbar = tk.Scrollbar(listbox_frame, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Contenedor de botones
        button_container = tk.Frame(self.main_container, bg=self.glass_bg)
        button_container.pack(pady=20, padx=40)
        
        # Botones épicos
        self.create_epic_button(button_container, "➕ Agregar", self.agregar_tarea, 0)
        self.create_epic_button(button_container, "✓ Completar", self.marcar_completada, 1)
        self.create_epic_button(button_container, "🗑 Eliminar", self.eliminar_tarea, 2)
        
        # Contador de tareas
        self.task_counter = tk.Label(
            self.main_container,
            text="0 tareas pendientes",
            font=("Segoe UI", 10),
            fg=self.secondary_text,
            bg=self.glass_bg
        )
        self.task_counter.pack(pady=5)
        
        # Iniciar animación de partículas
        self.animate_particles()
        
    def draw_gradient_background(self):
        """Dibuja un gradiente épico en el fondo"""
        for i in range(650):
            ratio = i / 650
            if ratio < 0.5:
                r = int(15 + (48 - 15) * (ratio * 2))
                g = int(12 + (43 - 12) * (ratio * 2))
                b = int(41 + (99 - 41) * (ratio * 2))
            else:
                r = int(48 + (36 - 48) * ((ratio - 0.5) * 2))
                g = int(43 + (36 - 43) * ((ratio - 0.5) * 2))
                b = int(99 + (62 - 99) * ((ratio - 0.5) * 2))
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, 900, i, fill=color)
    
    def create_particles(self):
        """Crea partículas flotantes para el fondo"""
        for _ in range(30):
            x = tk.IntVar(value=int(tk._default_root.winfo_screenwidth() * tk._default_root.call('expr', 'rand()')))
            y = tk.IntVar(value=int(650 * tk._default_root.call('expr', 'rand()')))
            size = 2 + int(3 * tk._default_root.call('expr', 'rand()'))
            particle = self.canvas.create_oval(
                x.get(), y.get(), x.get() + size, y.get() + size,
                fill=self.accent_color, outline=""
            )
            self.particles.append({
                'id': particle,
                'x': x.get(),
                'y': y.get(),
                'speed': 0.2 + 0.5 * tk._default_root.call('expr', 'rand()'),
                'size': size
            })
    
    def animate_particles(self):
        """Anima las partículas flotantes"""
        for particle in self.particles:
            particle['y'] -= particle['speed']
            if particle['y'] < -10:
                particle['y'] = 660
                particle['x'] = int(900 * tk._default_root.call('expr', 'rand()'))
            
            self.canvas.coords(
                particle['id'],
                particle['x'], particle['y'],
                particle['x'] + particle['size'], particle['y'] + particle['size']
            )
        
        self.root.after(50, self.animate_particles)
    
    def create_epic_button(self, parent, text, command, column):
        """Crea un botón con estilo épico"""
        btn_frame = tk.Frame(parent, bg="#2d2d44", highlightthickness=0)
        btn_frame.grid(row=0, column=column, padx=10)
        
        btn = tk.Button(
            btn_frame,
            text=text,
            font=("Segoe UI", 11, "bold"),
            bg="#2d2d44",
            fg=self.text_color,
            activebackground=self.accent_color,
            activeforeground="#000000",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=command,
            width=12,
            height=2
        )
        btn.pack(padx=2, pady=2)
        
        # Efectos hover
        btn.bind("<Enter>", lambda e: self.on_button_hover(btn, True))
        btn.bind("<Leave>", lambda e: self.on_button_hover(btn, False))
        
        return btn
    
    def on_button_hover(self, button, entering):
        """Efecto hover para botones"""
        if entering:
            button.config(bg=self.accent_color, fg="#000000")
        else:
            button.config(bg="#2d2d44", fg=self.text_color)
    
    def on_entry_focus_in(self, event):
        """Limpia el placeholder al hacer focus"""
        if self.entry.get() == "Escribe una nueva tarea...":
            self.entry.delete(0, tk.END)
            self.entry.config(fg=self.text_color)
    
    def on_entry_focus_out(self, event):
        """Restaura el placeholder si está vacío"""
        if self.entry.get() == "":
            self.entry.insert(0, "Escribe una nueva tarea...")
            self.entry.config(fg=self.secondary_text)
    
    def agregar_tarea(self):
        """Agrega una nueva tarea"""
        tarea = self.entry.get()
        if tarea != "" and tarea != "Escribe una nueva tarea...":
            self.listbox.insert(tk.END, f"  ○  {tarea}")
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Escribe una nueva tarea...")
            self.entry.config(fg=self.secondary_text)
            self.update_counter()
            self.flash_effect()
        else:
            messagebox.showwarning("⚠ Advertencia", "Por favor escribe una tarea válida.")
    
    def eliminar_tarea(self):
        """Elimina la tarea seleccionada"""
        try:
            seleccion = self.listbox.curselection()[0]
            self.listbox.delete(seleccion)
            self.update_counter()
            self.flash_effect()
        except IndexError:
            messagebox.showwarning("⚠ Advertencia", "Selecciona una tarea para eliminar.")
    
    def marcar_completada(self):
        """Marca la tarea como completada"""
        try:
            seleccion = self.listbox.curselection()[0]
            tarea = self.listbox.get(seleccion)
            
            if "✓" not in tarea:
                tarea_limpia = tarea.replace("○", "").strip()
                self.listbox.delete(seleccion)
                self.listbox.insert(tk.END, f"  ✓  {tarea_limpia}")
                self.update_counter()
                self.flash_effect()
        except IndexError:
            messagebox.showwarning("⚠ Advertencia", "Selecciona una tarea para marcar.")
    
    def update_counter(self):
        """Actualiza el contador de tareas"""
        total = self.listbox.size()
        completadas = sum(1 for i in range(total) if "✓" in self.listbox.get(i))
        pendientes = total - completadas
        self.task_counter.config(text=f"{pendientes} pendientes | {completadas} completadas | {total} total")
    
    def flash_effect(self):
        """Efecto flash al agregar/eliminar tareas"""
        original_bg = self.main_container.cget("bg")
        self.main_container.config(bg="#303050")
        self.root.after(100, lambda: self.main_container.config(bg=original_bg))

# Crear la aplicación
root = tk.Tk()
try:
    root.iconbitmap('icon.ico')
except:
    pass

app = EpicTaskManager(root)
root.mainloop()