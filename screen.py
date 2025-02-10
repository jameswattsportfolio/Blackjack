from PIL import Image, ImageTk
from tkinter import filedialog as fd
import customtkinter as ctk
import os
import math
import sys
from blackjack import initialise_deck

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

ball_image = ImageTk.PhotoImage(
    Image.open(cur_dir + "/images/roulette_pill.png").resize((10, 10)),
    (10, 10))

# Ball initial position
global ball_x
global ball_y
ball_x = 194
ball_y = 53

blackjack_canvas.create_image(ball_x,
                              ball_y,
                              image=ball_image,
                              anchor="nw",
                              tags="ball")


# Leaving commented as this is useful to get coordinates
def set_ball_x_coords(x):
    global ball_x, ball_y
    ball_x = x
    blackjack_canvas.moveto("ball", ball_x)
    print("New coordinates: (", ball_x, ", ", ball_y, ")")


def set_ball_y_coords(y):
    global ball_x, ball_y
    ball_y = y
    blackjack_canvas.moveto("ball", y=ball_y)
    print("New coordinates: (", ball_x, ", ", ball_y, ")")


coordinate_finder_x = ctk.CTkSlider(root,
                                    from_=0,
                                    to=912,
                                    command=set_ball_x_coords,
                                    width=912)
coordinate_finder_x.pack()
coordinate_finder_y = ctk.CTkSlider(root,
                                    from_=0,
                                    to=526,
                                    command=set_ball_y_coords,
                                    width=526)
coordinate_finder_y.pack()

# Establish the card images
for card in initialise_deck():
    card_image = ImageTk.PhotoImage(
        Image.open(cur_dir + f"/images/Playing Cards/{card}.png").resize(
            (60, 85)), (60, 85))
    blackjack_canvas.create_image(426,
                                  330,
                                  image=card_image,
                                  anchor="nw",
                                  tag=card,
                                  state="hidden")

face_down_card = ImageTk.PhotoImage(
    Image.open(cur_dir + f"/images/Playing Cards/face_down.png").resize(
        (60, 85)), (60, 85))
blackjack_canvas.create_image(426,
                              330,
                              image=face_down_card,
                              anchor="nw",
                              tag="face_down",
                              state="hidden")

global bet_amount
bet_amount, balance = 100, 1000
blackjack_canvas.create_text(770,
                             467,
                             fill="white",
                             font="Arial",
                             anchor="nw",
                             text=bet_amount,
                             tags="bet_amount")

blackjack_canvas.create_text(725,
                             420,
                             fill="white",
                             anchor="nw",
                             font="Arial",
                             text=f"Balance: {balance}",
                             tags="balance")


def decrease_bet():
    global bet_amount
    interval = 0
    match bet_amount:
        case bet if bet > 10 and bet <= 100:
            interval = 10
        case bet if bet > 100 and bet <= 500:
            interval = 50
        case bet if bet > 500 and bet <= 1000:
            interval = 100
        case bet if bet > 1000:
            interval = 1000
        case _:
            # Leave it as is
            interval

    bet_amount -= interval
    blackjack_canvas.itemconfigure("bet_amount", text=bet_amount)


def increase_bet():
    global bet_amount
    interval = 0
    match bet_amount:
        case bet if bet >= 0 and bet < 100:
            interval = 10
        case bet if bet >= 100 and bet < 500:
            interval = 50
        case bet if bet >= 500 and bet < 1000:
            interval = 100
        case bet if bet >= 1000 and bet < 10000:
            interval = 1000
        case _:
            # Leave it as is
            interval

    bet_amount += interval
    blackjack_canvas.itemconfigure("bet_amount", text=bet_amount)


decrease_bet_button = ctk.CTkButton(root,
                                    text="-",
                                    width=24,
                                    height=24,
                                    corner_radius=0,
                                    command=decrease_bet)

increase_bet_button = ctk.CTkButton(root,
                                    text="+",
                                    width=24,
                                    height=24,
                                    corner_radius=0,
                                    command=increase_bet)

blackjack_canvas.create_window(725,
                               482,
                               window=decrease_bet_button,
                               anchor="nw",
                               tags="decrease_bet_window")
blackjack_canvas.create_window(725,
                               447,
                               window=increase_bet_button,
                               anchor="nw",
                               tags="increase_bet_window")

if "pytest" not in sys.modules:
    # This opens the GUI so do not run it when testing
    root.mainloop()
