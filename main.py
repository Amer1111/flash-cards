from tkinter import *
import pandas as pd
from random import choice
import os

BACKGROUND_COLOR = "#B1DDC6"
lang_to_learn = "French"
lang_you_know = "English"
random_pair = {}
data_dict = []

# ---------------------------- Read words ----------------------- #
def read_data():
    global random_pair
    global data_dict

    try:
        data_to_learn_df = pd.read_csv("./data/french_words_to_learn")
        print("french_words_to_learn found. Reading....")
    except FileNotFoundError:
        print("french_words_to_learn NOT found. Reading from french_words....")
        data_original_df = pd.read_csv("./data/french_words.csv")
        data_dict = data_original_df.to_dict(orient="records")
    else:
        data_dict = data_to_learn_df.to_dict(orient="records")
    finally:
        print(data_dict)
        random_pair = choice(data_dict)
read_data()
# ---------------------------- Button functions ----------------------- #
# FLIP TO THE BACK OF THE CARD TO SHOW THE ANSWER AFTER 3 SECONDS
def translate():
    canvas.itemconfig(canvas_image, image=card_back_img)
    language_label.config(text=lang_you_know)
    random_word_you_know = random_pair[lang_you_know]
    word_label.config(text=random_word_you_know)


def generate_new_word():
    global random_pair
    try:
        random_pair = choice(data_dict)
    except IndexError:  # IF WE RUN OUT OF WORDS GO BACK TO THE ORIGINAL FILE TO START OVER
        answer = input("You learned all the words! Time to restart or expand your library of words. "
                       "\n\nIf you would like to restart with the "
                       "original library of words type y else type n to exit: ").lower()
        if answer == "y":
            os.remove("./data/french_words_to_learn")
            print("empty file 'french_words_to_learn' deleted successfully.")
            read_data()
        else:
            exit()
    else:
        random_word_to_learn = random_pair[lang_to_learn]
        canvas.itemconfig(canvas_image, image=card_front_img)
        language_label.config(text=lang_to_learn)
        word_label.config(text=random_word_to_learn)
        screen.after(3000, func=translate)


# FLIP TO THE FRONT OF THE CARD TO SHOW A NEW WORD
def right():
    print("Well done! You knew this combo:")
    print(random_pair)
    # UPDATE "WORD TO LEARN" file
    data_dict.remove(random_pair)
    print("Word has been removed from the learning file. Here are the remaining:")
    print(data_dict)
    data_to_learn_df = pd.DataFrame(data_dict)
    data_to_learn_df.to_csv("./data/french_words_to_learn", index=False)
    generate_new_word()


def wrong():
    print("You did not know this combo: ")
    print(random_pair)
    generate_new_word()


# ---------------------------- UI SETUP ------------------------------- #
screen = Tk()
screen.title("Flash Cards: French to English")
screen.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

screen.after(3000, func=translate)

# BUTTONS
right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, command=right, highlightthickness=0, bg=BACKGROUND_COLOR)
right_button.grid(column=1, row=2)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, command=wrong, highlightthickness=0, bg=BACKGROUND_COLOR)
wrong_button.grid(column=3, row=2)

# CANVAS (FRONT AND BACK OF CARD)
canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(800, 526, anchor="se", image=card_front_img)
canvas.grid(row=1, column=0, columnspan=5)

# LABELS
language_label = Label(text=lang_to_learn, font=("Ariel", 40, "italic"), bg="white")
language_label.place(x=400, y=150, anchor="center")

word_label = Label(text=random_pair[lang_to_learn], font=("Ariel", 60, "bold"), bg="white")
word_label.place(x=400, y=263, anchor="center")

screen.mainloop()
