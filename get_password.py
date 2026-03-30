import tkinter as tk
import remote_connection

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
    
    label     = tk.Label (prompt_dialog_box, text="Message ")
    text_area = tk.Text  (prompt_dialog_box)
    button    = tk.Button(prompt_dialog_box, text="OK", command=lambda:on_click_OK_for_question(text_area, prompt_dialog_box) )

    label.pack(side="top")
    button.pack(side="bottom")
    text_area.pack()
        
   # password_dialog_box.grab_set()
    prompt_dialog_box.focus_set()
    text_area.focus_set()
    
# for security purpose 
    main_frame.wait_window(prompt_dialog_box)

    print("the string message cmd: ", str_msg_cmd)

   
    return str_msg_cmd






def send_msg_single(main_frame, term_btn, username, password):

    small_msg = get_msg_details(main_frame)

    print("got message", small_msg)
#    resutl = remote_connection.run_sudo_cmd(client, cmd, username, password)
    final_msg = f'''GUI_USER=$(loginctl list-sessions --no-legend | awk '$4=="seat0" {{print $3; exit}}');
    GUI_UID=$(id -u "$GUI_USER");
    [ -n "$GUI_USER" ] && sudo -u "$GUI_USER" DISPLAY=:0 XDG_RUNTIME_DIR=/run/user/$GUI_UID notify-send "{small_msg}"
    '''
   # connect_default(final_msg)
    try:
        remote_connection.run_sudo_cmd(term_btn. client, final_msg, username, password)
    except Exception as e:
        traceback.print_exc()

def lock_screen_single(main_frame, term_btn, username, password):


#    resutl = remote_connection.run_sudo_cmd(client, cmd, username, password)
    final_msg = "sudo loginctl lock-sessions"
   # connect_default(final_msg)
    try:
        remote_connection.run_sudo_cmd(term_btn. client, final_msg, username, password)
    except Exception as e:
        traceback.print_exc()

def shut_down_single(main_frame, term_btn, username, password):


#    resutl = remote_connection.run_sudo_cmd(client, cmd, username, password)
    final_msg = "sudo shutdown now"
   # connect_default(final_msg)
    try:
        remote_connection.run_sudo_cmd(term_btn. client, final_msg, username, password)
    except Exception as e:
        traceback.print_exc()



def on_click_OK_single_host(option, holding_frame):


    print("This is the output", option)
     
def options_for_single_host(image_dict, main_frame, term_btn, username, password):

    
    single_host_box= tk.Toplevel(main_frame)
    single_host_box.title("machine INFO")
    single_host_box.geometry("250x300")
    single_host_box.resizable(True, True)
    
    label     = tk.Label (single_host_box, text="Message ")
    cmd_entry = tk.Entry (single_host_box, text="command")
    button    = tk.Button(single_host_box, text="OK", command=lambda:on_click_OK_for_question(text_area, prompt_dialog_box) )
    msg_btn   = tk.Button(single_host_box, text="Msg", command=lambda:send_msg_single(main_frame, term_btn, username, password))
    cmd_btn   = tk.Button(single_host_box, text="CMD")
    lock_btn  = tk.Button(single_host_box, text="Lock", command=lambda:lock_screen_single(main_frame, term_btn, username, password))
    shut_down_btn=tk.Button(single_host_box,text="Shutdown", command=lambda:shut_down_single(main_frame, term_btn, username, password))
    
    label.pack(side="top")
    cmd_entry.pack(side="top")
    cmd_btn.pack(side="top")
    msg_btn.pack(side="top")
    lock_btn.pack(side="top")
    shut_down_btn.pack(side="top")
    button.pack(side="top")
        
   # password_dialog_box.grab_set()
    single_host_box.focus_set()
    
# for security purpose 
    main_frame.wait_window(single_host_box)

    print("the string message cmd: ", str_msg_cmd)

   
    return str_msg_cmd



main_frame = tk.Tk()
main_frame.geometry("500x500")

button  = tk.Button(main_frame, text="get dialog", command=lambda : options_for_single_host(main_frame))
button.pack()


main_frame.mainloop()

#password =  get_password(main_frame)


