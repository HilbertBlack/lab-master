import tkinter as tk

password=""

def on_click_OK(entry, holding_frame):
    global password
    password = entry.get()
    print("Password: ", password)
    holding_frame.destroy()
     
def get_password(main_frame):

    global password
    
    password_dialog_box = tk.Toplevel(main_frame)
    password_dialog_box.title("Password Please")
    password_dialog_box.geometry("250x100")
    password_dialog_box.resizable(False, False)
    
    label = tk.Label(password_dialog_box, text="Enter your password: ")
    entry = tk.Entry(password_dialog_box, show="*")
    button= tk.Button(password_dialog_box, text="OK", command=lambda:on_click_OK(entry,password_dialog_box) )

    label.pack()
    button.pack(side="right", padx=10)
    entry.pack()
        
   # password_dialog_box.grab_set()
    password_dialog_box.focus_set()
    entry.focus_set()
    
# for security purpose 
    main_frame.wait_window(password_dialog_box)

    print("Got password: ", password)

   
    return password


str_msg_cmd = ""

def on_click_OK_for_question(text_area, holding_frame):
    global str_msg_cmd
    str_msg_cmd = text_area.get("1.0","end")
    print(" ", str_msg_cmd)
    
    holding_frame.destroy()
     
def get_msg_details(main_frame):

    global str_msg_cmd
    
    prompt_dialog_box = tk.Toplevel(main_frame)
    prompt_dialog_box.title("Write Message ")
    prompt_dialog_box.geometry("250x300")
    prompt_dialog_box.resizable(False, False)
    
    label     = tk.Label (prompt_dialog_box, text="Enter your password: ")
    text_area = tk.Text  (prompt_dialog_box)
    button    = tk.Button(prompt_dialog_box, text="OK", command=lambda:on_click_OK_for_question(text_area, prompt_dialog_box) )

    label.pack(side="top")
    button.pack(side="right", padx=10)
    text_area.pack()
        
   # password_dialog_box.grab_set()
    prompt_dialog_box.focus_set()
    text_area.focus_set()
    
# for security purpose 
    main_frame.wait_window(prompt_dialog_box)

    print("the string message cmd: ", str_msg_cmd)

   
    return str_msg_cmd



# main_frame = tk.Tk()
# main_frame.geometry("500x500")
# 
# button  = tk.Button(main_frame, text="get dialog", command=lambda : get_password(main_frame))
# button.pack()
# 
# 
# main_frame.mainloop()
# password =  get_password(main_frame)


