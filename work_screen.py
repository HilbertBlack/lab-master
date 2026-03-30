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


current_date = datetime.date.today()
current_time = datetime.datetime. now().strftime("%H_%M")
print("staring date:", current_date, " starting time:", current_time)

os.makedirs(f"./logs/{current_date}/{current_time}", exist_ok=True)

common_user = "user"
common_pass = "password"

isSUDO = None

missing_ips_list = set()
connected_ips_list = set()

client_list_to_term_btn_dict = {}

array_of_term_btns = []
list_of_ips = []
list_of_clients = []
list_of_lists = []

term_screen=None
ctrl_screen=None

isSUDO_check_box=None

connect_btn = None
cmd_btn     = None
copy_btn    = None
msg_btn     = None
lock_btn    = None
shut_down_btn=None

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

MESSAGE_ICON = tk.PhotoImage(file="./images/message.png")
LOCK_ICON    = tk.PhotoImage(file="./images/lock.png")
SHUTDOWN_ICON= tk.PhotoImage(file="./images/shutdown.png")

image_dict = { "MESSAGE_ICON": MESSAGE_ICON, "LOCK_ICON": LOCK_ICON, "SHUTDOWN_ICON": SHUTDOWN_ICON}


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
        
def restructure(event):
    global array_of_term_btns, list_of_ips
    # print("got btns", len(array_of_term_btns))
    no_of_cols = event.width // array_of_term_btns[0].cover.winfo_width()

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

    global list_of_clients, connected_ips_list, missing_ips_list
    print("Number of IPs : ", len(list_of_ips))
    
    for ip in list_of_ips:

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
    print("no of client:",len(list_of_clients))

    reset_color_all_term_btns(YELLOW_ICON)

    global list_of_lists
    
    list_of_lists = []
    
    for client in list_of_clients:
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


def lock_sessions_all():
    global list_of_clients

    lock_cmd = "sudo loginctl lock-sessions"
    print("the LOCK cmd = ", lock_cmd)

    run_cmd_all(list_of_clients, lock_cmd, username_entry.get(), password_entry.get(), isSUDO=True)

def shut_down_all():
    global list_of_clients

    shutdown_cmd = "sudo loginctl shutdown now"
    print("the LOCK cmd = ", lock_cmd)

    run_cmd_all(list_of_clients, lock_cmd, username_entry.get(), password_entry.get(), isSUDO=True)


def get_credentials():

    global username_entry, password_entry
    
    print("user: ",username_entry.get())
    print("password: ",password_entry.get())

def initialize(main_frame):
    global term_screen, ctrl_screen, array_of_term_btns, list_of_ips, list_of_clients,  username_entry, password_entry, isSUDO

    array_of_term_btns = []
    list_of_ips = json_reader.read_file("./ips.json")  # this function return only the list of the ips scanned
    
    term_screen = tk.Frame(main_frame, bg="#2e3436")
    ctrl_screen = tk.Frame(main_frame, bg="#555753")

    cmd_entry   = tk.Entry(main_frame)
    
    #
    # buttons for the left panel
    # getting the ips count from the file
    get_term_btn()
    #
    # buttons for the right panel
    # once all the button is load we can try to connect or exec command

    username_label = tk.Label(ctrl_screen, text = "User name:")
    username_entry = tk.Entry(ctrl_screen)
    username_entry.insert(0,common_user)
    password_label = tk.Label(ctrl_screen, text = "Password:")
    password_entry = tk.Entry(ctrl_screen, show = "*")
    password_entry.insert(0,common_pass)

    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()

    main_frame.update()
    
    connect_btn = tk.Button(ctrl_screen, text = "Connect", command=lambda : connect_all(list_of_ips, username_entry.get(), password_entry.get()))
    # connect_btn = tk.Button(ctrl_screen, text = "Connect", command = connect_default)

    isSUDO = tk.BooleanVar()
    isSUDO_check_box = tk.Checkbutton(ctrl_screen, text="is SUDO", command=lambda: print_SUDO_status(isSUDO) , variable = isSUDO)
    cmd_btn     = tk.Button(ctrl_screen, text = "CMD", command=lambda: run_cmd_all(
                                                                                    list_of_clients, 
                                                                                    cmd_entry.get().strip(),
                                                                                    username_entry.get(), 
                                                                                    password_entry.get(),  
                                                                                    isSUDO.get()
                                                                                ))
    copy_btn    = tk.Button(ctrl_screen, text = "Copy")
    msg_btn     = tk.Button(ctrl_screen, text = "Msg", command = send_msg_all)
    lock_btn    = tk.Button(ctrl_screen, text = "Lock",command = lock_sessions_all)
    shut_down_btn=tk.Button(ctrl_screen, text = "Shut Down", command = shut_down_all)

    connect_btn.pack(fill= "x",pady=5)
    isSUDO_check_box.pack()
    cmd_btn.pack(fill= "x",pady=5)
    msg_btn.pack(fill= "x",pady=5)
    copy_btn.pack(fill= "x",pady=5)
    lock_btn.pack(fill = "x", pady=5)
    shut_down_btn.pack(fill = "x", pady=5)

    cmd_entry.place(relx=0, rely=0, relwidth=1)
    cmd_entry.insert(0,"Command to execute")

    main_frame.update()
    
    y_position = cmd_entry.winfo_height()
    print("y_position: ", y_position)
    term_screen.place(relx=0,    y=y_position, relwidth=0.85, relheight=1)
    ctrl_screen.place(relx=0.85, y=y_position, relwidth=0.15, relheight=1)

    
initialize(main_frame)


# green_btn = term_lm(term_screen, "192.168.136.100", GREEN_ICON )
# grey_btn  = term_lm(term_screen, "192.168.136.101", GREY_ICON)
# red_btn   = term_lm(ctrl_screen, "192.168.136.102", RED_ICON)
# yellow_btn= term_lm(ctrl_screen, "192.168.136.103", YELLOW_ICON)
# 

term_screen.bind("<Configure>", restructure)

main_frame.mainloop()
