import tkinter as tk
import json as json
import re as re
from tkinter import filedialog
from pathlib import Path

list_of_hosts = []
list_of_ips   = []

def read_json_file(file_name):

    global list_of_ips, list_of_hosts

    file = open(file_name)

    if(file == None):
        print("File does not exit!!!")
        return -1
    print("File Opened Successfully")

    
    list_of_hosts = json.load(file)
    

    for element in list_of_hosts:
        print(str(element.get("ip")))

        list_of_ips.append( str( element.get("ip")))

    return list_of_ips

def read_txt_file(file_name):

    global list_of_ips, list_of_hosts

    ip_pattern = r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$"
    
    with open(file_name, "r") as file:

        for line in file:
            line = line.strip()
            if re.match(ip_pattern, line):
                print(line)
                list_of_ips.append(line)
            else:
                print("This is NOT a valid ip address:", line)
                continue

    return list_of_ips




def get_src_file_path(input_file_prompt, src_file_path):

    temp = filedialog.askopenfilename(title="Select src file", parent=input_file_prompt)
    print("select input ips file :", temp)
    src_file_path.set( temp )
    
    return src_file_path.get()
     

def select_path_btn_click(holding_frame, src_file_path, error_label):

    file_path = Path( src_file_path.get() )

    if not file_path.exists():
        error_label.config(text="enter a valid file path")
        return -1

    print("File exists !!!")

    holding_frame.destroy()
        

def read_any_file(main_frame):

    src_file_path = tk.StringVar(value="")  
    
    input_file_prompt = tk.Toplevel(main_frame)

    input_file_prompt.title("Select input file")
    input_file_prompt.geometry("300x200")
    input_file_prompt.resizable(False, False)

    select_file_label = tk.Label (input_file_prompt, text="source file:")
    src_select_btn    = tk.Button(input_file_prompt, text="src", command= lambda: get_src_file_path(input_file_prompt, src_file_path))
    src_path_entry    = tk.Entry (input_file_prompt, textvariable=src_file_path)
    select_btn        = tk.Button(input_file_prompt, text="Selct", command= lambda: select_path_btn_click(input_file_prompt, src_file_path, error_label))
    error_label       = tk.Label(input_file_prompt, text="", fg="red")

    select_file_label.pack(side="left", anchor="n", pady=(20, 0))
    src_path_entry.pack(side="top",padx=(0,10), pady=(20, 0), fil="x")
    error_label.pack(side="top")
    src_select_btn.pack(side="top")
    select_btn.pack(side="right", anchor="s")

    # input_file_prompt.lift()
    # input_file_prompt.focus_force()
    input_file_prompt.attributes("-topmost", True) 
    input_file_prompt.after(100, lambda: input_file_prompt.attributes("-topmost",False))
    # input_file_prompt.focus_set()
    src_path_entry.focus_set()
    main_frame.wait_window(input_file_prompt)

    

    file = Path(src_file_path.get()).expanduser()
    
    if ( file.exists() ) :
        print(f"Reading from {str(file)}")
    else:
        print("File not found!!!\n")
        return -1

    if (file.suffix == ".json"):
        return read_json_file(file)
    elif (file.suffix == ".txt"):
        return read_txt_file(file)
    
