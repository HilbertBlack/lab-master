import traceback as traceback
import tkinter as tk
import paramiko as paramiko
import os as os
import datetime as datetime
import remote_connection as remote_connection
import json_reader as json_reader
import find_user as find_user
import window_functions as window_functions
import get_password 
import rearrange as rearrange
from tkinter import font
from tkinter import filedialog


current_date = datetime.date.today()
current_time = datetime.datetime. now().strftime("%H_%M")
print("staring date:", current_date, " starting time:", current_time)

os.makedirs(f"./logs/{current_date}/{current_time}", exist_ok=True)

common_user = "user"
common_pass = "password"

isSUDO = None
isSTFM = 0
toSTOP = 0

missing_ips_list = set()
connected_ips_list = set()

client_list_to_term_btn_dict = {}

array_of_term_btns = []
list_of_ips = []
list_of_clients = []
list_of_lists = []
list_of_elements = []

term_screen=None
ctrl_screen=None
canvas_screen=None


isSUDO_check_box=None

connect_btn = None
cmd_btn     = None
copy_btn    = None
msg_btn     = None
lock_btn    = None
shut_down_btn=None

short_form_btn =None
help_btn       =None
exit_btn       =None

src_file_label=None
des_file_label=None

src_browse_btn=None
des_browse_btn=None

username_entry =None
password_entry =None
cmd_entry      =None

main_frame = tk.Tk()
main_frame.title("Lab master")
main_frame.geometry("800x600")
main_frame.resizable(True, True)

#
# there is a change made here
#need to check of any fault occurs
DEFAULT_ICON_SIZE = (105,90)

GREEN_ICON = tk.PhotoImage(file="./images/green.png").subsample(5)
GREY_ICON  = tk.PhotoImage(file="./images/grey.png").subsample(5)
RED_ICON   = tk.PhotoImage(file="./images/red.png").subsample(5)
YELLOW_ICON= tk.PhotoImage(file="./images/yellow.png").subsample(5)
RED_CROSS_ICON = tk.PhotoImage(file="./images/redCross.png").subsample(5)

MESSAGE_ICON = tk.PhotoImage(file="./images/message.png").subsample(12)
LOCK_ICON    = tk.PhotoImage(file="./images/lock.png").subsample(12)
SHUTDOWN_ICON= tk.PhotoImage(file="./images/shutdown.png").subsample(12)
RUN_ICON     = tk.PhotoImage(file="./images/run.png").subsample(14)
COPY_ICON    = tk.PhotoImage(file="./images/clip_board.png").subsample(14)

UNLOCK_USER_ICON  = tk.PhotoImage(file="./images/unlock_user.png").subsample(12)
LOCK_USER_ICON    = tk.PhotoImage(file="./images/lock_user.png").subsample(12)

image_dict = { "MESSAGE_ICON": MESSAGE_ICON, "LOCK_ICON": LOCK_ICON, "SHUTDOWN_ICON": SHUTDOWN_ICON}

src_file_path = tk.StringVar(value="src  file")
des_file_path = tk.StringVar(value="des  file ")


class term_btn:

    # components related to GUI
    main_frame = None
    term_btn   = None
    icon_img   = None
    caption    = None
    cover      = None

    # components related to the remote machine
    client      = None
    hostname    = ""
    ip_address  = None
    active_users= None
    conn_status = "not_conn"
    
    def __init__(self, main_frame, ip_address, image = GREY_ICON):

        self.main_frame = main_frame 
#
#   for the lwft panel button
#
        self.cover = tk.Frame(main_frame, bg= "green")
        
        self.icon_img = image
        self.term_btn = tk.Button(self.cover, image=self.icon_img, width=105, height=90, command= lambda: get_password.options_for_single_host(image_dict, main_frame, self, username_entry.get(), password_entry.get()))
        self.term_btn.image = self.icon_img
        self.caption  = tk.Label(self.cover, text=ip_address, width=14) 
        self.ip_address= ip_address
        
        self.term_btn.pack(side="left")
        self.caption.pack(side="top")

        self.cover.pack(side="left")

    def set_user_list(self, list_of_users):
       
        self.active_users = list_of_users
        net_str = self.hostname[:10] + "\n" + self.ip_address 

        count = 0
        for user in list_of_users:
            if (user[1] == "ssh"):
                conn_type = "[R] "
            elif(user[1] == "local"):
                conn_type = "[L] "
            net_str =  net_str + "\n" + conn_type+ user[0]
            count= count + 1
            if(count == 3):
                break
        self.caption.config(text=net_str)
        print("...........changing the user list ...............")
        #self.caption.config(text = "new\nnew")

    def unpack_caption(self):
        self.caption.pack_forget()
    def pack_caption(self):
        self.caption.pack(side="top")
        

def get_term_btn():

    global list_of_lists, array_of_term_btns
    
    print(list_of_ips)
    
    for ip in list_of_ips:
        temp_term_btn = term_btn(term_screen, ip, GREY_ICON)
        array_of_term_btns.append(temp_term_btn)
    
def change_term_btn_icon(ip_address, icon_status):

    global array_of_term_btns
 
    print("CHANGING THE COLOR OF:",ip_address)
    print("list of terminal buttons:", len(array_of_term_btns))
    for t_btn in array_of_term_btns:
        if(t_btn.ip_address == ip_address):
            t_btn.term_btn.config(image=icon_status)

            t_btn.icon_img = icon_status
            
            t_btn.term_btn.image = icon_status

            if(icon_status == GREEN_ICON):
                t_btn.conn_status = "alive"
            elif (icon_status == GREY_ICON):
                t_btn.conn_status = "not_conn"
            elif (icon_status == RED_CROSS_ICON):
                t_btn.conn_status = "not_conn"
            else:
                t_btn.conn_status = "alive"
            
            break

    main_frame.update()

def print_SUDO_status(isSUDO):
    print("is SUDO :", isSUDO.get())

def set_term_btn_client(ip_address, client):

    global array_of_term_btns
     
    print("list of terminal buttons:", len(array_of_term_btns))
    for t_btn in array_of_term_btns:
        if(t_btn.ip_address == ip_address):
            t_btn.client = client
            break

    print("=== mapped ",ip_address, " to correct term box ===")

def set_term_btn_users(ip_address, list_of_users):

    global array_of_term_btns
    for t_btn in array_of_term_btns:
        if(t_btn.ip_address == ip_address):
            t_btn.set_user_list(list_of_users)
            break

    print("=== mapped ",ip_address, "with the correct users_list ===")

def set_term_btn_hostname(ip_address, hostname):
    global array_of_term_btns
    for t_btn in array_of_term_btns:
        if(t_btn.ip_address == ip_address):
            t_btn.hostname = hostname.strip()
            break

    print("=== mapped ",hostname, "with the correct machine name ===")

def reset_color_all_term_btns(icon_status):
    for t_btn in array_of_term_btns:
    
        if(t_btn.conn_status == "alive"):

            t_btn.term_btn.config(image=icon_status)
            t_btn.icon_img = icon_status            
            t_btn.term_btn.image = icon_status
            
    print("colour reseted")

    main_frame.update()
### -----------------------------------------
def restructure(event):
    global array_of_term_btns, list_of_ips, term_screen, canvas_screen
    # print("got btns", len(array_of_term_btns))

    term_screen.update_idletasks()

    no_of_cols = term_screen.winfo_width() // array_of_term_btns[0].cover.winfo_width()
    no_of_rows = (len(array_of_term_btns) // no_of_cols) + (len(array_of_term_btns) % no_of_cols)
    
    x=0
    y=0
    count = 0
    
    for btn in array_of_term_btns:
        #print("x:",x,"y:",y)
        btn.cover.place(x=x,y=y)
        x = x + btn.cover.winfo_width()
        count = count + 1
        if (count == no_of_cols):
            count = 0
            x = 0
            y = y + btn.cover.winfo_height()   


    term_screen.config(height=y+btn.cover.winfo_height())
    
    term_screen.update_idletasks()
    
    canvas_screen.configure(
        scrollregion=canvas_screen.bbox("all")
    )
### --------------------------------------------
def grid_restructure(event):
    global list_of_elements

    #print("before :", len(list_of_elements))
    #rearrange.grid_arrange(ctrl_screen, list_of_elements)
    rearrange.ribbon_style(ctrl_screen, list_of_elements)

def short_long_form(array_of_term_btns):

    global isSTFM 
    
    if (isSTFM == 0):
        isSTFM = 1
        for btn in array_of_term_btns:
            btn.unpack_caption()
    else:
        isSTFM = 0
        for btn in array_of_term_btns:
            btn.pack_caption()


    restructure(None)

    
def get_initial_data(client):

    list_of_users = []

    hostname = "hostname"
    init_cmd = "w -h"
    
    stdin, stdout, stderr = remote_connection.run_cmd(client, init_cmd)
    #ip_address = client.get_transport().getpeername()[0]
    out_content = stdout.read().decode()

    t_stdin, t_stdout, t_stderr = remote_connection.run_cmd(client, "hostname")
    hostname = t_stdout.read().decode()

    exit_code   = stdout.channel.recv_exit_status()
    t_exit_code = t_stdout.channel.recv_exit_status()
        
    if(exit_code == 0 and t_exit_code == 0):
        ## success
        init_data_list = find_user.parse_w_to_dict(out_content)
        print(init_data_list)
        for one_user in init_data_list:
            if ("ssh" in one_user['cmd']):
                conn_type = "ssh"
            else:
                conn_type = "local"
            list_of_users.append([one_user['user'], conn_type])

    else:
        print("-------- obtained initial data failed ----------")
    return list_of_users, hostname
    
def connect_all(list_of_ips, common_username, common_password):

    global list_of_clients, connected_ips_list, missing_ips_list, toSTOP
    print("Number of IPs : ", len(list_of_ips))
    
    for ip in list_of_ips:
        if(toSTOP == 1):
            toSTOP = 0
            print("\n\nstoped the connected process\n\n")
            break;

        if(ip in connected_ips_list):
            continue
        
        temp_client = paramiko.SSHClient()
        temp_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print("Trying to connect:", ip)
            temp_client.connect(hostname = ip, username = common_username, password = common_password, port = 22)
            list_of_clients.append(temp_client)
            print("connected: ", ip)

            set_term_btn_client(ip, temp_client)

            list_of_users, hostname = get_initial_data(temp_client)
            print("{ list users }")
            print(list_of_users)

            set_term_btn_hostname(ip, hostname)
            set_term_btn_users(ip, list_of_users)
            
            connected_ips_list.add(ip)
            missing_ips_list.discard(ip)

            change_term_btn_icon( ip, GREEN_ICON)
            
        except Exception as e:
            print("Connection failed :", ip) 
            change_term_btn_icon(ip, RED_CROSS_ICON)
            print("Exception:", repr(e))

            traceback.print_exc()

            missing_ips_list.add(ip)
            connected_ips_list.discard(ip)
            
            # this part if the number of user is comparetelivy more 
            # print("writting to the missing_ips.list file")
            # with open("missing_ips.list", "a") as f:
            #     f.write(ip)

    main_frame.update()
            
    return list_of_clients


def connect_missing_ips():

    print(" ; adding missing client ; ")
    missing_ips_list_copy = missing_ips_list.copy()

    connect_all(missing_ips_list_copy, common_username, common_password)

    print("Missing list")
    
def close_all(list_of_clients):
    if(len(list_of_clients) == 0):
        print("No active client now")   
        return -1
    else:
        for client in list_of_clients:
            client.close()
         
def run_cmd_all(list_of_clients, cmd, username, password, isSUDO):
    global toSTOP
    print("no of client:",len(list_of_clients))

    reset_color_all_term_btns(YELLOW_ICON)

    global list_of_lists
    
    list_of_lists = []
    
    for client in list_of_clients:

        if(toSTOP == 1):
            toSTOP = 0
            print("\n\nstoped the RUN CMD process\n\n")
            break;
    
        stdin = stdout = stderr = None
        ip_address = client.get_transport().getpeername()[0]
        if (isSUDO == False):
            stdin, stdout, stderr = remote_connection.run_cmd(client, cmd)
        else:
            stdin, stdout, stderr = remote_connection.run_sudo_cmd(client, cmd, username, password)

        content = ""
        errors  = ""
        print("client:", client.get_transport().getpeername()[0])
        print(" ===== content =====")
        for line in stdout:
            print(line, end="")
            content += line

        print(" ===== errors =====")
        for line in stderr:
            print(line, end="")
            errors += line

        exit_code = stdout.channel.recv_exit_status()
    
        if(exit_code == 0):
            print("success!!!")
            change_term_btn_icon(ip_address, GREEN_ICON)
        else:
            print("{ FAILED }")
            change_term_btn_icon(ip_address, RED_ICON)

        print("EXIT CODE: ", exit_code)

        list_of_lists.append([ip_address, stdin, stdout, stderr, exit_code])

        with open(f"./logs/{current_date}/{current_time}/{ip_address}", "a") as f:
            cmd_str = "CMD_EXECUTED = " + cmd + "\n"
            f.write(cmd_str)
            f.write(content)
            f.write(errors)
            exit_str = "EXIT_CODE: " + str(exit_code) + "\n"
            f.write(exit_str)
        
    return list_of_lists

def connect_default(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname = "10.198.122.106", username = "machine", password = "machine@123", port = 22)

    print("client connected")

    stdin, stdout, stderr, exit_code = remote_connection.run_sudo_cmd(client, cmd, "machine", "machine@123")

    print("output: ", stdout.read().decode())
    print("Exit code: ", stdout.channel.recv_exit_status())
    client.close()

def send_msg_all():
    global list_of_clients

#     str_msg_cmd = window_functions.pop_up_question_for_send_msg(main_frame)
#   
#     print("Sending messages with command ->", window_functions._str_msg_cmd)
# 
#     run_cmd_all(list_of_clients, window_functions._str_msg_cmd, common_user, common_pass, isSUDO = False)

    str_msg_cmd = get_password.get_msg_details(main_frame)
    if(str_msg_cmd == ""):
        print("SMPTY STRING")
        return -1

    print("P ",str_msg_cmd," P")    
    # final_msg = f'''GUI_USER=$(loginctl list-sessions --no-legend | awk '$4=="seat0" {{print $3; exit}}'); \
    # [ -n "$GUI_USER" ] && sudo -u "$GUI_USER" DISPLAY=:0 XAUTHORITY=/home/$GUI_USER/.Xauthority zenity --info --text="{str_msg_cmd} & disown" || echo "No active GUI session"'''

    final_msg = f'''GUI_USER=$(loginctl list-sessions --no-legend | awk '$4=="seat0" {{print $3; exit}}');
    GUI_UID=$(id -u "$GUI_USER");
    [ -n "$GUI_USER" ] && sudo -u "$GUI_USER" DISPLAY=:0 XDG_RUNTIME_DIR=/run/user/$GUI_UID notify-send "{str_msg_cmd}"
    '''
    
    print("final : ", final_msg)

   # connect_default(final_msg)
    try:
        run_cmd_all(list_of_clients, final_msg, username_entry.get(), password_entry.get(), isSUDO = True )
    except Exception as e:
        traceback.print_exc()

def copy_all():
    global list_of_clients, src_file_path, des_file_path

    if(src_file_path.get() == "" or des_file_path.get() == ""):
        print("File not specified")
        return -1 
        
    for client in list_of_clients:
        ip_address = client.get_transport().getpeername()[0]
        copy_result = remote_connection.copy_file(client, src_file_path.get(), des_file_path.get())
        if ( copy_result == -1 ):
            change_term_btn_icon(ip_address,  RED_ICON)

        elif ( copy_result == 0):
            change_term_btn_icon(ip_address, GREEN_ICON)
    return 0
    

def lock_user():
    global list_of_clients
    username = get_password.get_username(main_frame)
    
    lock_user_cmd = "sudo passwd -l " + username
    print("the LOCK user  cmd = ", lock_user_cmd)

    run_cmd_all(list_of_clients, lock_user_cmd, username_entry.get(), password_entry.get(), isSUDO=True)

def unlock_user():
    global list_of_clients
    username = get_password.get_username(main_frame)

    unlock_user_cmd = "sudo passwd -u " + username
    print("the UNLOCK user cmd = ", unlock_user_cmd)

    run_cmd_all(list_of_clients, unlock_user_cmd, username_entry.get(), password_entry.get(), isSUDO=True)


def lock_sessions_all():
    global list_of_clients

    lock_cmd = "sudo loginctl lock-sessions"
    print("the LOCK cmd = ", lock_cmd)

    run_cmd_all(list_of_clients, lock_cmd, username_entry.get(), password_entry.get(), isSUDO=True)

def shut_down_all():
    global list_of_clients

    shutdown_cmd = "sudo loginctl shutdown now"
    print("the LOCK cmd = ", shutdown_cmd)

    run_cmd_all(list_of_clients, lock_cmd, username_entry.get(), password_entry.get(), isSUDO=True)

def get_credentials():

    global username_entry, password_entry
    
    print("user: ",username_entry.get())
    print("password: ",password_entry.get())

def get_src_file_path():

    global src_file_path
    
    selected_file = filedialog.askopenfilename()

    print("SOURCE SELECTED: ", selected_file)
    
    src_file_path.set( selected_file )

def get_des_file_path():

    global des_file_path
    
    selected_file = filedialog.askopenfilename()

    print("DESTINATION SELECTED: ", selected_file)
    
    des_file_path.set( selected_file )

    
def initialize(main_frame):
    global term_screen, ctrl_screen, canvas_screen,  array_of_term_btns, list_of_ips, list_of_clients, list_of_elements, username_entry, password_entry, isSUDO

    array_of_term_btns = []
    list_of_ips = json_reader.read_file("./ips.json")  # this function return only the list of the ips scanned


    canvas_plus_scroll_bar = tk.Frame(main_frame, bg="red")
    canvas_screen          = tk.Canvas(canvas_plus_scroll_bar, bg="#2e3436")
    term_screen_scroll_bar = tk.Scrollbar(canvas_plus_scroll_bar,
                                          orient=tk.VERTICAL, 
                                          command=canvas_screen.yview
                                         )

    
    term_screen = tk.Frame(canvas_screen, bg="#2e3436")
    ctrl_screen = tk.Frame(main_frame, bg="#555753")


### ---------------------------------------------
    canvas_window = canvas_screen.create_window((0,0),anchor="nw",window=term_screen)

    def resize_canvas(event):
        canvas_screen.itemconfig(canvas_window, width=event.width)

    canvas_screen.bind("<Configure>", resize_canvas)    

    canvas_screen.configure(yscrollcommand=term_screen_scroll_bar.set)   
    term_screen_scroll_bar.configure(command=canvas_screen.yview)
    
    term_screen.bind("<Configure>", lambda e: canvas_screen.configure(scrollregion=canvas_screen.bbox("all")))        
        
### ---------------------------------------------

    # sep_u_r     = tk.Frame(main_frame, width = 2, bg = "red")
    # sep_r_i     = tk.Frame(main_frame, width = 2, bg = "black")
    # sep_i_c     = tk.Frame(main_frame, width = 2, bg = "black")
    # sep_c_o     = tk.Frame(main_frame, width = 2, bg = "black")

    connection_frame = tk.Frame(ctrl_screen)
    command_frame    = tk.Frame(ctrl_screen)
    info_frame       = tk.Frame(command_frame)
    copy_Frame       = tk.Frame(ctrl_screen)
    other_Frame      = tk.Frame(ctrl_screen)
        
    # cmd_entry   = tk.Entry(main_frame)
    cmd_entry   = tk.Entry(command_frame)

    # buttons for the left panel
    # getting the ips count from the file
    get_term_btn()

    # buttons for the right panel
    # once all the button is load we can try to connect or exec command

    custom_font = font.nametofont("TkDefaultFont").copy()
    custom_font.configure(size=11)

    username_label = tk.Label(connection_frame, text = "User name:", font=custom_font)
    username_entry = tk.Entry(connection_frame                     , font=custom_font)
    username_entry.insert(0,common_user)
    password_label = tk.Label(connection_frame, text = "Password:" , font=custom_font)
    password_entry = tk.Entry(connection_frame, show = "*"         , font=custom_font)
    password_entry.insert(0,common_pass)

    src_file_label = tk.Entry(copy_Frame, textvariable=src_file_path, font=custom_font)
    des_file_label = tk.Entry(copy_Frame, textvariable=des_file_path, font=custom_font)

    short_form_btn = tk.Button(other_Frame, text="shfm", command=lambda: short_long_form(array_of_term_btns))
    help_btn       = tk.Button(other_Frame, text="Help")
    exit_btn       = tk.Button(other_Frame, text="Exit")

    main_frame.update()

    connect_btn = tk.Button(connection_frame, text = "Connect", command=lambda : connect_all(list_of_ips, username_entry.get(), password_entry.get()))
    # connect_btn = tk.Button(ctrl_screen, text = "Connect", command = connect_default)

    isSUDO = tk.BooleanVar()
    isSUDO_check_box = tk.Checkbutton(info_frame, text="is SUDO", command=lambda: print_SUDO_status(isSUDO) , variable = isSUDO)
    cmd_btn     = tk.Button(info_frame, text = "CMD", command=lambda: run_cmd_all(
                                                                                    list_of_clients, 
                                                                                    cmd_entry.get().strip(),
                                                                                    username_entry.get(), 
                                                                                    password_entry.get(),  
                                                                                    isSUDO.get()
                                                                                ))
    copy_btn    = tk.Button(copy_Frame, text = "Copy", command = copy_all)
    msg_btn     = tk.Button(info_frame, text = "Msg", command = send_msg_all)
    lock_btn    = tk.Button(info_frame, text = "Lock",command = lock_sessions_all)
    shut_down_btn =tk.Button(info_frame, text = "Shut Down", command = shut_down_all)
    lock_usr_btn  =tk.Button(info_frame, text = "lock user", command =  lock_user )
    unlock_usr_btn=tk.Button(info_frame, text = "unlock user", command= unlock_user)

    src_browse_btn = tk.Button(copy_Frame, text="src", command = get_src_file_path)
    des_browse_btn = tk.Button(copy_Frame, text="des", command = get_des_file_path)

    msg_btn.config(image = MESSAGE_ICON)
    lock_btn.config(image= LOCK_ICON)
    shut_down_btn.config(image=SHUTDOWN_ICON)
    copy_btn.config(image=COPY_ICON)
    cmd_btn.config(image =RUN_ICON)
    lock_usr_btn.config(image=LOCK_USER_ICON)
    unlock_usr_btn.config(image=UNLOCK_USER_ICON)

    msg_btn.image       = MESSAGE_ICON
    lock_btn.image      = LOCK_ICON
    shut_down_btn.image = SHUTDOWN_ICON
    copy_btn.image      = COPY_ICON
    cmd_btn.image       = RUN_ICON
    lock_usr_btn.image  = LOCK_USER_ICON
    unlock_usr_btn.image= UNLOCK_USER_ICON

    # list_of_elements = [
    # username_label, username_entry, password_label, password_entry, connect_btn, sep_u_r,
                # cmd_entry, isSUDO_check_box, cmd_btn, sep_r_i,
    # src_file_label, src_browse_btn, des_file_label, des_browse_btn,copy_btn, sep_i_c,
                # msg_btn,lock_btn,shut_down_btn, sep_i_c
            # ]

    #cmd_entry.place(relx=0, rely=0, relwidth=1)
    #cmd_entry.insert(0,"Command to execute")

    main_frame.update()
    # rearrange.grid_arrange(main_frame, list_of_elements)
   
    #y_position = cmd_entry.winfo_height()
    #print("y_position: ", y_position)

    rearrange.basic_frame_h_pack(info_frame,     [isSUDO_check_box, cmd_btn, msg_btn, lock_btn, unlock_usr_btn, lock_usr_btn,  shut_down_btn])


    rearrange.basic_frame_v_pack(connection_frame, [username_label, username_entry, password_label, password_entry, connect_btn])
    rearrange.basic_frame_v_pack(command_frame,    [cmd_entry, info_frame ])
    rearrange.basic_frame_hv_pack(copy_Frame,      [[src_browse_btn, src_file_label], [des_browse_btn, des_file_label], [copy_btn]])
    rearrange.basic_frame_v_pack(other_Frame,      [short_form_btn, help_btn, exit_btn])
    
    connection_frame.pack(side="left",anchor="n")
    command_frame.pack(side="left", anchor="n", fill="x", expand=True)
    other_Frame.pack(side="right", anchor="n")
    copy_Frame.pack(side="right", anchor="n")
    
    ctrl_screen.place(relx=0, rely=0, relwidth=1, relheight=0.25)
    canvas_plus_scroll_bar.place(relx=0, rely=0.25, relwidth=1, relheight=0.75)

    term_screen_scroll_bar.pack(side="right", fil="y")
    canvas_screen.pack(side="left", fil="both", expand=True)

initialize(main_frame)

term_screen.bind("<Configure>", restructure)
ctrl_screen.bind("<Configure>", grid_restructure)

restructure(None)
main_frame.mainloop()
