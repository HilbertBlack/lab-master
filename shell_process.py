import subprocess
from tkinter import Entry


cmd_stdout = None

def run_cmd(cmd, cmd_input=""):
    global cmd_stdout

    if (isinstance(cmd,str)):
        cmd_with_args_as_list = cmd.split(' ')
        print(" Found as raw string")
    elif (isinstance(cmd, list)):
        cmd_with_args_as_list = cmd
        print("Found as list")
    elif (isinstance(cmd, Entry)):
        cmd_with_args_as_list = cmd.get().split(' ')
        print("Foundn as tkinter entry element")

        
    process = subprocess.Popen(
                cmd_with_args_as_list,
                stdout=subprocess.PIPE,
                stdin = subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )


    
    cmd_stdout = process.stdout

    if ( cmd_input != "" ):
        process.stdin.write(cmd_input+'\n')
    elif(isinstance(cmd_input,list)):
        for arg in cmd_input:
            process.stdin.write(arg + '\n')
    
    #return the object instance
    return cmd_stdout

# 
# 
# for line in stdout:
    # print(line, end="")

    process.wait()



run_cmd()
