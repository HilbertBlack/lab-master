import paramiko
import os
import pty
import select
import sys
import termios
import tty

host = "192.168.1.4"
username = "machine"
password = "machine@123"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)

# Open interactive shell
channel = client.invoke_shell()

# Save terminal settings
oldtty = termios.tcgetattr(sys.stdin)
tty.setraw(sys.stdin)
tty.setcbreak(sys.stdin)

try:
    while True:
        r, w, e = select.select([channel, sys.stdin], [], [])

        if channel in r:
            data = channel.recv(1024)
            if len(data) == 0:
                break
            sys.stdout.write(data.decode())
            sys.stdout.flush()

        if sys.stdin in r:
            x = sys.stdin.read(1)
            if not x:
                break
            channel.send(x)

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
    client.close()
