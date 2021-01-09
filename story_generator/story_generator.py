import os
import sys
import time
import easygui as g

working_dir = os.path.dirname(os.path.realpath(__file__))

def feed_me():
    title = "Text Generator"
    msg = "Enter your choice of preferences"
    field_names = ("Name of main character", "Place where events happen")
    field_values = []
    field_values = g.multenterbox(msg,title, field_names)

    while True:
        if field_values == None:
            break
        err_msg = ""
        for i in range(len(field_names)):
            if field_values[i].strip() == "":
                err_msg = err_msg + f"{field_names[i]} is a mandatory field.\n\n"
        if err_msg == "": break # no problems found
        field_values = g.multenterbox(err_msg, title, field_names, field_values)
    
    return field_values

# match_of_my_life.txt
def show_text(output, main_character, place):
    if output == "Adventure of Lifetime":
        with open(working_dir + "/adventure_of_lifetime.txt", 'r') as f:
            raw_txt = f.readlines()

        clean_txt = ""
        for i in raw_txt:
            i = str(i).replace('our_character', str(main_character)).replace('our_place', str(place))
            clean_txt += i
    elif output == "Match of my Life":
        with open(working_dir + "/match_of_my_life.txt", 'r') as f:
            raw_txt = f.readlines()

        clean_txt = ""
        for i in raw_txt:
            i = str(i).replace('our_character', str(main_character)).replace('our_place', str(place))
            clean_txt += i
    else:
        with open(working_dir + "/devastating_experience.txt", 'r') as f:
            raw_txt = f.readlines()

        clean_txt = ""
        for i in raw_txt:
            i = str(i).replace('our_character', str(main_character)).replace('our_place', str(place))
            clean_txt += i
    
    return clean_txt

while True:
    title = "Text Generator"
    text = "Select one of the titles below"
    choices = ("Adventure of Lifetime", "Match of my Life", "Devastating Experience")

    output = g.choicebox(msg=text, title=title, choices=choices)
    output = str(output)
    
    if output == "Adventure of Lifetime":
        field_values = feed_me()

        # Text depending on user input
        message = show_text(output, field_values[0], field_values[1])
        msg = g.msgbox(message, output)
    elif output == "Match of my Life":
        field_values = feed_me()

        # Text depending on user input
        message = show_text(output, field_values[0], field_values[1])
        msg = g.msgbox(message, output)
    elif output == "Devastating Experience":
        field_values = feed_me()

        # Text depending on user input
        message = show_text(output, field_values[0], field_values[1])
        msg = g.msgbox(message, output)
    else:
        pass

    # -----------------------------------
    msg = "Do you want to continue?"
    title = "Please Confirm"

    if g.ynbox(msg, title):
        pass
    else:
        sys,exit(0)
