import tkinter as tk
import remote_connection
import shell_process
import configparser as configparser

password=""
username=""


no_of_users=0
list_of_new_users = []
list_of_old_users = []
# OPEN_EYE = tk.PhotoImage(file="./images/open_eye.png")


config = configparser.ConfigParser()
config.read("./config.ini")


print(config.get("system_cmd","LOCK_SCREEN"))

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
    print("The message:", str_msg_cmd)
    
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


# this part is get the username to lock or unlock from
# admin username this function will return entered in
# the popup window


def on_click_OK_for_username(username_entry, holding_frame):

    global username
    
    username = username_entry.get()
    print(" ", str_msg_cmd)
    
    holding_frame.destroy()

    return username
    
def get_username(main_frame):

    global username
    
    username_dialog_box = tk.Toplevel(main_frame)
    username_dialog_box.title("username")
    username_dialog_box.geometry("250x100")
    username_dialog_box.resizable(False, False)
    
    label = tk.Label(username_dialog_box, text="Enter the username: ")
    entry = tk.Entry(username_dialog_box)
    button= tk.Button(username_dialog_box, text="OK", command=lambda:on_click_OK_for_username(entry,username_dialog_box) )

    label.pack()
    button.pack(side="right", padx=10)
    entry.pack()
        
   # password_dialog_box.grab_set()
    username_dialog_box.focus_set()
    entry.focus_set()
    
# for security purpose 
    main_frame.wait_window(username_dialog_box)

    print("Got username b: ", username)

   
    return username

# get the username and the new password from the administator and 
# display it in the window with a + button to add more buttons
# added new users flag variables will be incremented

def see_unsee_passwd(entry):

    show_config = entry.cget("show")
    if (show_config == "*"):
        entry.config(show="")
    else:
        entry.config(show="*")

def add_small_window_for_change_passwd(main_frame):

    # upon creating a small windows 
    # it returns username, pass1, pass2 , error
    # elements within that small window 

    global no_of_users
    
    small_frame = tk.Frame(main_frame)

    error_label    = tk.Label(small_frame, text="wrong!!! check password", fg="red")
    username_label = tk.Label(small_frame, text="Username:")
    username_entry = tk.Entry(small_frame)

    passwd_label_1 = tk.Label(small_frame,text="New password:")
    d_frame_1      = tk.Frame(small_frame)
    passwd_entry_1 = tk.Entry(d_frame_1, show="*")
    eye_btn_1      = tk.Button(d_frame_1,text="e1", command=lambda: see_unsee_passwd(passwd_entry_1))

    passwd_label_2 = tk.Label(small_frame,text="Retype password:")
    d_frame_2      = tk.Frame(small_frame)
    passwd_entry_2 = tk.Entry(d_frame_2, show="*")
    eye_btn_2      = tk.Button(d_frame_2,text="e2", command=lambda: see_unsee_passwd(passwd_entry_2))


    username_label.pack(side="top")
    username_entry.pack(side="top")
    error_label.pack(side="top") ; error_label.pack_forget()
    passwd_label_1.pack(side="top") 
    d_frame_1.pack(side="top")    
    passwd_entry_1.pack(side="left"); eye_btn_1.pack(side="left")
    passwd_label_2.pack(side="top")
    d_frame_2.pack(side="top")
    passwd_entry_2.pack(side="left"); eye_btn_2.pack(side="left")

    separator_line = tk.Frame(small_frame, height=2, bg="black", pady=2)
    separator_line.pack(side="top", fill="x")
    
    small_frame.pack(side="top", padx=10)

    no_of_users = no_of_users + 1
    print("a new frame is added || users:", no_of_users)

# attaching all the elements to the frame

    return [username_entry, passwd_entry_1, passwd_entry_2, error_label]

def on_click_OK_for_change_passwd(holding_frame, list_of_small_window):

    # first check "new password" and "retype password" are same
    print("no of users ", len(list_of_small_window))
    global list_of_new_users
    isAll_correct = 1
    
    for small_frame in list_of_small_window:
        if (small_frame[0].get().strip() == ""):
            print("empty username field")
        
        if(small_frame[1].get() == small_frame[2].get()):
            print("correct password for ", small_frame[0].get())
            small_frame[3].pack_forget()
        else:
            print("wrong password for ", small_frame[0].get())
            small_frame[3].pack(before=small_frame[0])
            isAll_correct = 0

    if (isAll_correct == 1):
        print("all are correct")

        list_of_new_users = []
        
        for small_frame in list_of_small_window:            
            list_of_new_users.append([small_frame[0].get(), small_frame[1].get()])    

        holding_frame.destroy()

        return list_of_new_users
        
    else:
        print("password are wrong for few users")
    
def get_new_passwd(main_frame):
    # This function returns a list [n, [username, password], [username, password], ...]
    # also manages it UI by it small function names add_small_window
    # the starting count to 1 upon running for one time initialy
    
    global no_of_users, list_of_new_users

    list_of_small_window = []
    list_of_new_users    = []

    no_of_users = 0
    
    username_new_passwd_box = tk.Toplevel(main_frame)
    username_new_passwd_box.title("change password")
    username_new_passwd_box.resizable(False, False)


    base      = tk.Frame(username_new_passwd_box, bg="grey")
    add_btn   = tk.Button(base, text="+", command=lambda : list_of_small_window.append( add_small_window_for_change_passwd(username_new_passwd_box) )  )
    create_btn= tk.Button(base, text="change", command=lambda: on_click_OK_for_change_passwd(username_new_passwd_box,   list_of_small_window))

    base.pack(side="bottom", fill="x")
    add_btn.pack(side="left")
    create_btn.pack(side="right")

# running this to get the first prompt 

    list_of_small_window.append( add_small_window_for_change_passwd(username_new_passwd_box) )

    username_new_passwd_box.focus_set()
    main_frame.wait_window(username_new_passwd_box)

# this segement will run then 
# list of new users in the format of
# [ [name, passwd], [name,passwd], [...] ]

    return list_of_new_users


# -----------------------------------------------------------------

# This function is to get username from the admin
# for the deteing the users. only the username is need 
# if the username is wrong we get need to prevent other users deletion


def get_old_users(main_frame):
   
    
    list_of_small_window = []
    global list_of_old_users

    no_of_old_users = 0
    
    username_box = tk.Toplevel(main_frame)
    username_box.title("change password")
    username_box.resizable(False, False)


    base      = tk.Frame(username_box, bg="grey")
    add_btn   = tk.Button(base, text="+" , command = lambda: list_of_small_window.append( add_small_window_for_user_del(username_box) ))
    del_btn   = tk.Button(base, text="delete", command = lambda: on_click_OK_for_user_del(username_box ,list_of_small_window) )

    base.pack(side="bottom", fill="x")
    add_btn.pack(side="left")
    del_btn.pack(side="right")

# running this to get the first prompt 

    username_box.focus_set()
    main_frame.wait_window(username_box)

# this segement will run then 
# list of new users in the format of
# [username1, username2, ... ]

    return list_of_old_users


def add_small_window_for_user_del(main_frame):

    # upon creating a small windows 
    # it returns username, pass1, pass2 , error
    # elements within that small window 

    global no_of_users
    
    small_frame = tk.Frame(main_frame)

    error_label    = tk.Label(small_frame, text="wrong!!! check username", fg="red")
    username_label = tk.Label(small_frame, text="Username:")
    username_entry = tk.Entry(small_frame)


    username_label.pack(side="top")
    username_entry.pack(side="top")
    error_label.pack(side="top") ; error_label.pack_forget()

    separator_line = tk.Frame(small_frame, height=2, bg="black", pady=2)
    separator_line.pack(side="top", fill="x", pady=2)
    
    small_frame.pack(side="top", padx=10)

    no_of_users = no_of_users + 1
    print("a new frame is added || old_users:", no_of_users)

# attaching all the elements to the frame

    return [username_entry, error_label]


def on_click_OK_for_user_del(holding_frame, list_of_small_window):

    # In the future for error label will be added, but given here
    print("no of old users ", len(list_of_small_window))

    global list_of_old_users
    
    list_of_old_users = []
    
    for small_frame in list_of_small_window:
       list_of_old_users.append(small_frame[0].get())

    holding_frame.destroy()

    print("previous:", list_of_old_users)
    return list_of_old_users
        

# ------------------------------------------------------


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
    final_msg = config.get("system_cmd", "LOCK_SCREEN")
   # connect_default(final_msg)
    try:
        remote_connection.run_sudo_cmd(term_btn. client, final_msg, username, password)
    except Exception as e:
        traceback.print_exc()

def shut_down_single(main_frame, term_btn, username, password):


#    resutl = remote_connection.run_sudo_cmd(client, cmd, username, password)
    final_msg = config.get("system_cmd", "SHUT_DOWN_NOW")
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
    spawn_term   = tk.Button(single_host_box, text="spawn_term", command= lambda:shell_process.spawn_terminal_session_with_ssh(username, term_btn.ip_address))
    
    label.pack(side="top")
    cmd_entry.pack(side="top")
    cmd_btn.pack(side="top")
    msg_btn.pack(side="top")
    lock_btn.pack(side="top")
    shut_down_btn.pack(side="top")
    spawn_term.pack(side="top")
    button.pack(side="top")

    
   # password_dialog_box.grab_set()
    single_host_box.focus_set()
    
# for security purpose 
    main_frame.wait_window(single_host_box)

    print("the string message cmd: ", str_msg_cmd)

   
    return str_msg_cmd



# main_frame = tk.Tk()
# main_frame.geometry("500x500")
# 
# button  = tk.Button(main_frame, text="get dialog", command=lambda : options_for_single_host(main_frame))
# button.pack()
# 
# 
# main_frame.mainloop()

#password =  get_password(main_frame)


