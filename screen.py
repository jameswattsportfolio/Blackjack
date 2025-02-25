from math import floor
from PIL import Image, ImageTk
from tkinter import filedialog as fd
import customtkinter as ctk
import os
import random
import sys
from time import sleep
from blackjack import initialise_deck, deal_initial_hand, calc_total, draw_next_card

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

global card_images
card_images = []
# Establish the card images
for card in initialise_deck():
    card_image = ImageTk.PhotoImage(
        Image.open(cur_dir + f"/images/Playing Cards/{card}.png").resize(
            (60, 85)), (60, 85))
    card_images.append(card_image)

face_down_card = ImageTk.PhotoImage(
    Image.open(cur_dir + f"/images/Playing Cards/face_down.png").resize(
        (60, 85)), (60, 85))

# # Three face down car
# for i in range(3):
#     face_down_type = "deal" if i == 0 else "dealer" if i == 1 else "double"
# blackjack_canvas.create_image(426,
#                               330,
#                               image=face_down_card,
#                               anchor="nw",
#                               tag=f"face_down_dealer",
#                               state="hidden")
# blackjack_canvas.create_image(426,
#                               330,
#                               image=face_down_card,
#                               anchor="nw",
#                               tag=f"face_down_double",
#                               state="hidden")

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

global deck_in_play
deck_in_play = initialise_deck()
random.shuffle(deck_in_play)


def update_player_scores():
    global player_hands

    for hand in player_hands:
        score = calc_total(hand)
        index = player_hands.index(hand)
        blackjack_canvas.itemconfigure(f"player_score_{index}",
                                       state="normal",
                                       text=int(score))


def update_dealer_score():
    global dealer_hand
    score = calc_total(dealer_hand)
    blackjack_canvas.itemconfigure("dealer_score",
                                   state="normal",
                                   text=int(score))


def deal_cards_animation(cards, dest_xs, dest_ys, i=0, initial=False):
    dest_x, dest_y = dest_xs[0], dest_ys[0]
    card = cards[0]
    tag = "face_down_deal"
    stopping_index = int(floor(dest_y / 3.3))
    if i == 0:
        blackjack_canvas.moveto(tag, dest_x, 0)
        blackjack_canvas.itemconfigure(tag, state="normal")
        root.after(7, deal_cards_animation, cards, dest_xs, dest_ys, i + 1,
                   initial)
    elif i == stopping_index:
        # Hide the dealer's fist card

        card_state = "hidden" if len(cards) == 1 and initial else "normal"

        blackjack_canvas.moveto(tag, dest_x, dest_y)
        blackjack_canvas.itemconfigure(tag, state="hidden")

        global card_images
        card_image_index = initialise_deck().index(card)

        if len(cards) == 1 and initial:
            blackjack_canvas.create_image(dest_x,
                                          dest_y,
                                          image=face_down_card,
                                          anchor="nw",
                                          tag="face_down_dealer")
        else:
            blackjack_canvas.create_image(dest_x,
                                          dest_y,
                                          image=card_images[card_image_index],
                                          anchor="nw",
                                          tag=card,
                                          state=card_state)

        if len(cards) > 1:
            root.after(7, deal_cards_animation, cards[1:], dest_xs[1:],
                       dest_ys[1:], 0, initial)
        else:
            update_player_scores()
            show_available_buttons()
    else:
        blackjack_canvas.moveto(tag, dest_x, 0 + (3.3 * i))
        root.after(7, deal_cards_animation, cards, dest_xs, dest_ys, i + 1,
                   initial)


# def reveal_card_at(card, x, y):
#     print("Revealing card...")
#     print(card, x, y)
#     blackjack_canvas.moveto(card, x, y)
#     blackjack_canvas.itemconfigure(card, state="normal")


def draw_card():
    hide_user_actions()
    global player_hands, deck_in_play

    next_card, deck_in_play = draw_next_card(deck_in_play)
    card_number = len(player_hands[0])
    player_hands[0].append(next_card)
    deal_cards_animation([next_card], [426 + (card_number * 10)],
                         [330 - (card_number * 10)])

    # hitable = calc_total(player_hands[0]) < 21

    # if hitable:
    #     show_available_buttons()
    # else:
    #     dealers_turn()


def dealers_turn():
    update_dealer_score()
    hide_user_actions()

    global deck_in_play, player_hands, dealer_hand

    # Add the cards just played to the back of the deck
    deck_in_play = deck_in_play + [
        # Flatten player_hands
        card for hand in player_hands for card in hand
    ] + dealer_hand

    show_play_again_button()


def hide_user_actions():
    blackjack_canvas.delete("hit_window")
    blackjack_canvas.delete("stand_window")


def show_available_buttons():
    global player_hands, dealer_hand

    if "A" in dealer_hand[0]:
        # Ask for insurance
        pass

    hitable = calc_total(player_hands[0]) < 21
    doublable = len(player_hands[0]) == 2
    splitable = len(
        player_hands[0]
    ) == 2 and player_hands[0][0][:-1] == player_hands[0][1][:-1]

    if hitable:
        hit_button = ctk.CTkButton(root,
                                   text="Hit",
                                   width=80,
                                   height=24,
                                   corner_radius=0,
                                   command=draw_card)

        stand_button = ctk.CTkButton(root,
                                     text="Stand",
                                     width=80,
                                     height=24,
                                     corner_radius=0,
                                     command=dealers_turn)

        blackjack_canvas.create_window(405,
                                       460,
                                       window=hit_button,
                                       anchor="nw",
                                       tags="hit_window")

        blackjack_canvas.create_window(525,
                                       460,
                                       window=stand_button,
                                       anchor="nw",
                                       tags="stand_window")
    else:
        blackjack_canvas.delete("hit_window")
        blackjack_canvas.delete("stand_window")
        update_dealer_score()
        show_play_again_button()


def show_play_again_button():
    play_again_button = ctk.CTkButton(root,
                                      text="Play Again",
                                      width=80,
                                      height=24,
                                      corner_radius=0,
                                      command=begin_game)

    blackjack_canvas.create_window(405,
                                   460,
                                   window=play_again_button,
                                   anchor="nw",
                                   tags="play_again_window")


global player_hands, dealer_hand
player_hands = []
dealer_hand = []

face_down_card = ImageTk.PhotoImage(
    Image.open(cur_dir + f"/images/Playing Cards/face_down.png").resize(
        (60, 85)), (60, 85))

blackjack_canvas.create_image(426,
                              330,
                              image=face_down_card,
                              anchor="nw",
                              tag="face_down_deal",
                              state="hidden")

blackjack_canvas.create_text(448,
                             420,
                             fill="white",
                             font="Arial",
                             anchor="nw",
                             text="0",
                             state="hidden",
                             tags="player_score_0")

blackjack_canvas.create_text(448,
                             47,
                             fill="white",
                             font="Arial",
                             anchor="nw",
                             text="0",
                             state="hidden",
                             tags="dealer_score")


def remove_all_cards():
    for card in initialise_deck() + [
            # Don't need to delete the faced down card that gets delt
            "face_down_dealer",
            "face_down_double"
    ]:
        blackjack_canvas.delete(card)


def begin_game():
    remove_all_cards()
    blackjack_canvas.itemconfigure("decrease_bet_window", state="hidden")
    blackjack_canvas.itemconfigure("increase_bet_window", state="hidden")
    blackjack_canvas.delete("deal_window")
    blackjack_canvas.itemconfigure("play_again_window", state="hidden")
    blackjack_canvas.itemconfigure("player_score_0", state="hidden")
    blackjack_canvas.itemconfigure("dealer_score", state="hidden")

    global deck_in_play, player_hands, dealer_hand
    player_hands, dealer_hand, deck_in_play = deal_initial_hand(deck_in_play)

    # This is ordered in the way they are delt at the casino
    cards_to_deal = [
        player_hands[0][0], dealer_hand[0], player_hands[0][1], dealer_hand[1]
    ]

    deal_cards_animation(cards_to_deal, [426, 396, 436, 466],
                         [330, 80, 320, 80],
                         initial=True)


deal_button = ctk.CTkButton(root,
                            text="Deal",
                            width=80,
                            height=24,
                            corner_radius=0,
                            command=begin_game)

blackjack_canvas.create_window(405,
                               460,
                               window=deal_button,
                               anchor="nw",
                               tags="deal_window")

if "pytest" not in sys.modules:
    # This opens the GUI so do not run it when testing
    root.mainloop()
