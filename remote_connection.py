import paramiko 

#
# this funciton for running the non sudo command
#

def run_cmd(client, cmd):
    print("runing command :",cmd )
    
    stdin, stdout, stderr = client.exec_command(cmd)

    exit_code = stdout.channel.recv_exit_status()
    
    return [stdin, stdout, stderr, exit_code]

#
# this funciton for running the SUDO command
#

def run_sudo_cmd(client, cmd, username, password):

    print("running sudo command :", cmd)
    
    stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
    stdin.write(password+'\n')
    stdin.flush()

    exit_code = stdout.channel.recv_exit_status()
    
    return [stdin, stdout, stderr, exit_code]        


# creating a client instance
# client = paramiko.SSHClient()

# ADDING THIS COMPONENT TO SAVE THE HOST FOR FUTURE PURPOSESS
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# FINNALY CONNECTING TO THE HOST
# client.connect( hostname="192.168.137.25", username="gokul", password="Gokul@333", port=22)
# print("connected")
# 
# stdin, stdout, stderr, exit_code =run_sudo_cmd(client,"sudo -S whoami", "gokul", "Gokul@333")

# stdin, stdout, stderr =client.exec_command("sudo apt-get install neofetch -y", get_pty=True)
# 
# stdin.write("password\n")
# stdin.flush()

# output = stdout.read().decode()
# exit_code = stdout.channel.recv_exit_status()

# stdin, stdout, stderr, exit_code = run_sudo_cmd(client, "sudo apt-get install", "gokul", "password")

# print("output:", output)
# print("Exiting status :", exit_code)
# client.close()
