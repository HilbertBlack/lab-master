import tkinter as tk


screen   = None
label    = None
text_box = None
text_area= None
scan_btn = None
stop_btn = None


default_command =  "sudo -S masscan 192.168.136.0/24 -p22 -oL - -oJ ips.json"

def initialize(add_to_frame):
    global screen, label, text_box, scan_btn, stop_btn, text_box, text_area

    screen = tk.Frame(add_to_frame)

    label = tk.Label(screen,text="FAST SCAN",  bg="blue")

    scan_btn = tk.Button(screen, text="SCAN")
    
    text_box = tk.Entry(screen)
    text_box.insert(0, default_command);

    text_area = tk.Text(screen)
    
    label.pack(side="top", anchor="w")
    scan_btn.pack(side="top", anchor="e")
    text_box.pack(side="top", anchor="w", fill="x")
    text_area.pack(side="top", anchor="w", fill="both", expand=True,pady=10)
    
    screen.place(relwidth=1, relheight=1)
