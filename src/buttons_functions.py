import traceback
import remote_connection

def send_message_all(list_of_clients, status, msg):

    try:
        send_msg_cmd = f'zenity --{status} --text={msg}'

        print(f"~~~~~~ msg cmd :{send_msg_cmd} ~~~~~~~~")


    except Exception as e:
        print("got exception in message send all")
        traceback.print_exec()        
