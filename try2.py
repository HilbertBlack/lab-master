import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname="192.168.137.69", username="user", password="password")

# --- Run command
stdin, stdout, stderr = ssh.exec_command("ls")
print(stdout.read().decode())

# --- Open SFTP (same connection)
sftp = ssh.open_sftp()
sftp.put("/home/user/Desktop/notes.txt", "/home/user/notes.txt")
sftp.close()

# --- Run another command again
stdin, stdout, stderr = ssh.exec_command("whoami")
print(stdout.read().decode())

# --- Finally close everything
ssh.close()
