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

    label.pack(anchor="nw")
    entry.pack(anchor="center")
    button.pack(side="right", padx=10)
        
   # password_dialog_box.grab_set()
    password_dialog_box.focus_set()
    entry.focus_set()
    
# for security purpose 
    main_frame.wait_window(password_dialog_box)

    print("Got password: ", password)

   
    return password

# main_frame = tk.Tk()
# main_frame.geometry("500x500")
# 
# button  = tk.Button(main_frame, text="get dialog", command=lambda : get_password(main_frame))
# button.pack()
# 
# 
# main_frame.mainloop()
# password =  get_password(main_frame)


