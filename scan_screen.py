import tkinter as tk


screen=None
button_panel=None
reliable_scan_btn=None
fast_scan_btn=None


def initialize(add_to_frame):

    global screen, button_panel, reliable_scan, fast_scan_btn
    
    screen = tk.Frame(add_to_frame)

    button_panel = tk.Frame(screen, bg="cyan")

    reliable_scan_btn = tk.Button(button_panel, text="Reliable Scan")
    fast_scan_btn     = tk.Button(button_panel, text="Fast Scan")


    reliable_scan_btn.pack(fill="x")
    fast_scan_btn.pack(fill="x")

    
    button_panel.place(relx=0.5, rely=0.5, anchor="center")
    screen.place(relwidth=1, relheight=1)
