import time
from tkinter import *
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas







PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BACKGROUND_COLOR = "#B1DDC6"


window = Tk()
window.title(string="Flash Card Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


the_image = PhotoImage(file=r"\Users\LENOVO\PycharmProjects\flash-card-project-start\images\card_front.png")
right_image = PhotoImage(file=r"\Users\LENOVO\PycharmProjects\flash-card-project-start\images\right.png")
wrong_image = PhotoImage(file=r"\Users\LENOVO\PycharmProjects\flash-card-project-start\images\wrong.png")
back_image = PhotoImage(file=r"\Users\LENOVO\PycharmProjects\flash-card-project-start\images\card_back.png")

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)

front_image_canvas = canvas.create_image(400, 263, image=the_image)
# back_image_canvas = canvas.create_image(400, 263, image=back_image)

canvas.grid(columnspan=2, row=0)


title_card = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_card = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
data_dictionary = {}



original_data = pandas.read_csv("data.csv", on_bad_lines='skip')
data_dictionary = original_data.to_dict(orient="records")


current_card = {}
def pronounce():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get("https://youglish.com/")
    time.sleep(2)
    search = driver.find_element(By.CSS_SELECTOR, "form input")
    search.send_keys(f"{current_card['English']}")
    time.sleep(2)
    say_it = driver.find_element(By.CSS_SELECTOR, ".input-group button")
    say_it.click()






def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dictionary)
    canvas.itemconfig(word_card, text=current_card["English"], fill="black")
    canvas.itemconfig(title_card, text="English", fill="black")
    canvas.itemconfig(front_image_canvas, image=the_image)

    flip_timer = window.after(3000, flip_card)

def see_example():
    child_window = Toplevel(window)
    child_window.config(width=800, height=250)
    # word_label = Label(child_window, text=current_card["English"], font=("Ariel", 25, "normal"), fg=RED)
    # word_label.place(x=30, y=30)
    example_label = Label(child_window, text=f"1/.{current_card['Example']}", font=("Calibri", 20, "normal"))
    example_label.place(x=30, y=125)
    pronounce_button = Button(child_window, text=current_card["English"], font=("Ariel", 20, "normal"), fg=RED, command=pronounce)
    pronounce_button.place(x=30, y=30)

def show_data():
    os.startfile("data.csv")




def flip_card():
    canvas.itemconfig(front_image_canvas, image=back_image)
    canvas.itemconfig(word_card, text=current_card["Arabic"])
    canvas.itemconfig(title_card, text="Arabic")
    canvas.itemconfig(title_card, fill="white")
    canvas.itemconfig(word_card, fill="white")



#right button
right_button = Button(image=right_image, bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0, command=next_card)
right_button.grid(column=1, row=1)

#wrong button
example_button = Button(image=wrong_image, bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0, command=see_example)
example_button.grid(column=0, row=1)

#show data button
show = Button(text="SHOW DATA", command=show_data, bg=GREEN)
show.grid(row=2, column=0, columnspan=2)



flip_timer = window.after(3000, flip_card)


next_card()





window.mainloop()
