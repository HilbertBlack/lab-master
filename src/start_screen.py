import tkinter as tk
from tkinter import font

screen=None
button_panel=None
over_the_network_btn=None
row_col_btn=None


def initialize(add_to_parent_frame):

    global screen,  button_panel, over_the_network_btn, row_col_btn
    screen = tk.Frame(add_to_parent_frame, bg="red")

    button_panel = tk.Frame(screen, bg="cyan")

    default_font = font.nametofont("TkDefaultFont")
    custom_font  = default_font.copy()

    custom_font.configure(size=16)
    

    over_the_network_btn = tk.Button(button_panel, text="Over the Network", font=custom_font)
    row_col_btn          = tk.Button(button_panel, text="Row Col Network",  font=custom_font)


    over_the_network_btn.pack(fill="x")
    row_col_btn.pack(fill="x")

 #   button_panel.place(relx=0.5, rely=0.5, anchor="center")
    button_panel.place(relx=0.5, rely=0.5, anchor="center")
    screen.place(relwidth=1, relheight=1)
