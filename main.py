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
