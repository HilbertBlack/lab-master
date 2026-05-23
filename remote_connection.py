import paramiko 
import traceback
import time
from pathlib import Path
#
# this funciton for running the non sudo command
#

def run_cmd(client, cmd):
    print("runing command :",cmd )
    
    stdin, stdout, stderr = client.exec_command(cmd)

    #exit_code = stdout.channel.recv_exit_status()
    #exit_code = 1000
    return [stdin, stdout, stderr]

#
# this funciton for running the SUDO command
#

def run_sudo_cmd(client, cmd, username, password):

    print("running sudo command :", cmd)
    
    stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
    stdin.write(password+'\n')
    stdin.flush()

    #exit_code = stdout.channel.recv_exit_status()
    
    return [stdin, stdout, stderr]        



def run_cmd_inputs(client, cmd, inputs):

    print ("running cmd :", cmd)

    stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)

    for element in inputs:
        print("Giving input :", element)
        stdin.write(element)

    stdin.write("\n")
    stdin.flush()

    return  [stdin, stdout, stderr]
    
def run_sudo_cmd_inputs(client, cmd, username, password, inputs):

    print ("running sudo cmd :", cmd)

    stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
    time.sleep(1)
    stdin.write(password + '\n')
    
    print("password given")
    for element in inputs:
        time.sleep(1)
        print("Giving input :", element)
        stdin.write(element)
        
    stdin.flush()

    return  [stdin, stdout, stderr]
    

def copy_file(client, src_file_path, des_file_path):

    print("started copying to files")
    print("DST: ", des_file_path)

    try:
        ## opening sftp channel
        sftp_channel = client.open_sftp()
        attributes   = sftp_channel.put(src_file_path, des_file_path)
        sftp_channel.close()

    except Exception as e:
        print("File upload \033[31mFAILED\033[0m")
        print("Exception:". repr(e))
        traceback.print_exc()

        return -1
    print("finished copying")
    return 0 



# def copy_file(client, src_file_path, des_file_path):
# 
# 
#     try:
#         ## opening sftp channel
#         sftp_channel = client.open_sftp()
#         attributes   = sftp_channel.put(src_file_path, des_file_path)
#         sftp_channel.close()
# 
#     except Exception as e:
#         print("File upload \033[31mFAILED\033[0m")
#         print("Exception:". repr(e))
#         traceback.print_exc()

def download_file(client, src_file_path, des_file_path):

    des = ""
    try:
        des = Path(des_file_path).expanduser().resolve()

        des.parent.mkdir(parents=True, exist_ok=True)

        print("DST:",str(des))
     
    except Exception as e:
        print("<<<<<<< Directory creation failed >>>>>>>>")
        print("Exception:", repr(e))
        traceback.print_exc()
        return -1
        
    try:        
        ## opening sftp channel
        sftp_channel = client.open_sftp()
        attributes   = sftp_channel.get(src_file_path, str(des))
        sftp_channel.close()

        print("file creation successful")
        
        return 0
        
    except Exception as e:
        print("File download \033[31mFAILED\033[0m")
        print("Exception:", repr(e))
        traceback.print_exc()

        if des.exists():
            des.unlink()
            
    return -1

    
def download_folder(client, src_file_path, des_file_path):

   

    # cheching for the presence of the folder or file in the
    # remote path. First a sftp_client is opened, which will be used
    # for any file operation. stat(path) is used to check existance of the folder
    try :
    
        sftp_client = client.open_sftp()

        sftp_client.stat(src_file_path)

        print("src folder EXISTS!!!")
        # return 0


        if not os.path.exists(des_file_path):
            os.mkdir(local_dir)
        
        for filename in sftp_client.listdir(remote_dir):
            if stat.S_ISDIR(sftp_client.stat(remote_dir + filename).st_mode):
                # uses '/' path delimiter for remote server
                download_files(sftp_client, remote_dir + filename + '/', os.path.join(local_dir, filename))
            else:
                if not os.path.isfile(os.path.join(local_dir, filename)):
                    sftp_client.get(remote_dir + filename, os.path.join(local_dir, filename))
        

        
            
    except Exception as e:
        print("Found error while downloading folder ")
        print("Exception:", repr(e))
        traceback.print_exc()
        return -1



    




        
# # creating a client instance
# client = paramiko.SSHClient()
# 
# # ADDING THIS COMPONENT TO SAVE THE HOST FOR FUTURE PURPOSESS
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 
# 
# # FINNALY CONNECTING TO THE HOST
# client.connect( hostname="10.198.122.144", username="user", password="password", port=22)
# print("connected")
# 
# 
# # stdin, stdout, stderr = run_sudo_cmd(client,"kill", "user", "password")
# stdin, stdout, stderr =run_cmd(client,"bash ./Downloads/basic/script.sh")
# 
# # stdin, stdout, stderr =client.exec_command("sudo apt-get install neofetch -y", get_pty=True)
# #
# # stdin.write("password\n")
# # stdin.flush()
# 
# output = ""
# # output = stdout.read().decode()
# 
# for line in stdout:
    # print(line, end="")
    # output += line
    # 
# error  = stderr.read().decode()
# exit_code = stdout.channel.recv_exit_status()
# 
# # stdin, stdout, stderr, exit_code = run_sudo_cmd(client, "sudo apt-get install", "gokul", "password")
# 
# print(f"output({len(output)}):", output)
# print(f"error({len(error)}):", error)
# print("Exiting status :", exit_code)
# client.close()
