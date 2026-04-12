import paramiko 
import traceback
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


def copy_file(client, src_file_path, des_file_path):

    print("started copying to files")


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
