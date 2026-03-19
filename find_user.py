 
# sample output of w command
# 22:30:29 up 1 day, 12:54,  2 users,  load average: 0.85, 0.51, 0.50
# USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU  WHAT
# machine           10.16.32.62      22:17    3:48m  0.00s  0.04s sshd: machine [priv]
# manikand tty2     -                Tue09    3:48m  0.05s  0.05s /usr/libexec/gnome-session-binary --session=ubuntu



# for getting the list of currently logined into machine
# def get_user_list(lines):
# 
#     list_of_users = []
#     
#     list_lines = lines.split('\n')    
# 
#     for line in list_lines:
#         if(line == ""):
#             continue
#         print(line)
#         words = line.split()
#         print(words)
# 
#         list_of_users.append(words[0])
# 
#     print("users list")
#     print(list_of_users)
# 
# 
# def get_user_ip_list(lines):
#     list_of_users = []
#     
#     list_lines = lines.split('\n')    
# 
#     for line in list_lines:
#         if(line == ""):
#             continue
#         print(line)
#         words = line.split()
#         print(words)
# 
#         list_of_users.append(words[0])
# 
#     print("users list")
#     print(list_of_users)
#     


def parse_w_output(lines):
    for line in lines.strip().split("\n"):
        if not line.strip():
            continue

        parts = line.split()
        user = parts[0]

        # case 1: has tty (ttyX or pts/X)
        if len(parts) > 1 and (parts[1].startswith("tty") or parts[1].startswith("pts")):
            tty = parts[1]
            from_field = parts[2]
            idle = parts[4]

            # command starts from 6th field (index 5)
            cmd = " ".join(parts[5:])

        # case 2: no tty (shifted)
        else:
            tty = "N/A"
            from_field = parts[1]
            idle = parts[3]

            # command starts from 5th field (index 4)
            cmd = " ".join(parts[4:])

        # formatted output (like printf)
        print(f"{user:<10} {tty:<6} {from_field:<15} {idle:<6} {cmd}")



def parse_w_to_dict(lines):
    result = []

    for line in lines.strip().split("\n"):
        if not line.strip():
            continue

        parts = line.split()
        user = parts[0]

        if len(parts) > 1 and (parts[1].startswith("tty") or parts[1].startswith("pts")):
            tty = parts[1]
            from_field = parts[2]
            idle = parts[4]
            cmd = " ".join(parts[5:])
        else:
            tty = "N/A"
            from_field = parts[1]
            idle = parts[3]
            cmd = " ".join(parts[4:])

        result.append({
            "user": user,
            "tty": tty,
            "from": from_field,
            "idle": idle,
            "cmd": cmd
        })

    return result


# lines = '''
# machine           10.16.32.62      22:17    3:48m  0.00s  0.04s sshd: machine [priv]
# manikand tty2     -                Tue09    3:48m  0.05s  0.05s /usr/libexec/gnome-session-binary --session=ubuntu
# '''
# 
# parse_w_output(lines)
# result  = parse_w_to_dict(lines)
# 
# print(result)
