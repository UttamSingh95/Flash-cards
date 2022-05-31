from tkinter import *
import pandas
import random

# -------------- global veriest  ------------ #

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# -------------- file selection and exception  ------------ #

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# -------------- next card function  ------------ #

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_text, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background_image, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


# -------------- known card function  ------------ #

def is_know():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("website_data/words_to_learn.csv", index=False)
    next_card()


# -------------- flip card function  ------------ #

def flip_card():
    canvas.itemconfig(card_text, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background_image, image=card_back_image)


# -------------- creating window ------------ #

window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flashy")
flip_timer = window.after(3000, func=flip_card)

# -------------- UI creation  ------------ #
canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
card_background_image = canvas.create_image(400, 263, image=card_front_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
card_text = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))

cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="./images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_know)
known_button.grid(row=1, column=1)

# ---------------------------------------------------------------------------------- #

next_card()
window.mainloop()

