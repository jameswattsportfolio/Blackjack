from PIL import Image, ImageTk
from tkinter import filedialog as fd
import customtkinter as ctk
import os
import math
import sys

# Setup CustomTKinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

cur_dir = os.getcwd()

root = ctk.CTk()
root.title("Blackjack")
root.iconbitmap(cur_dir + "/images/dice.ico")
root.geometry("912x526")

# Establish CTK canvas and images
blackjack_canvas = ctk.CTkCanvas(root,
                                 width=912,
                                 height=526,
                                 borderwidth=0,
                                 bd=0,
                                 highlightthickness=0)
blackjack_canvas.pack(expand=True, fill="both")
bg_image = ImageTk.PhotoImage(
    Image.open(cur_dir + "/images/blackjack_table.jpg").resize((912, 526)),
    size=(912, 526))

blackjack_canvas.create_image(0, 0, image=bg_image, anchor="nw")

if "pytest" not in sys.modules:
    # This opens the GUI so do not run it when testing
    root.mainloop()
