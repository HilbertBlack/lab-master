import json as json
import re as re
from pathlib import Path


list_of_hosts = []
list_of_ips   = []

def read_json_file(file_name):

    global list_of_ips, list_of_hosts

    file = open(file_name)

    if(file == None):
        print("File does not exit!!!")
        return -1
    print("File Opened Successfully")

    list_of_hosts = json.load(file)


    for element in list_of_hosts:
        print(str(element.get("ip")))

        list_of_ips.append( str( element.get("ip")))

    return list_of_ips


def read_txt_file(file_name):

    global list_of_ips, list_of_hosts

    ip_pattern = r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$"
    
    with open(file_name, "r") as file:

        for line in file:
            line = line.strip()
            if re.match(ip_pattern, line):
                print(line)
                list_of_ips.append(line)
            else:
                print("This is NOT a valid ip address:", line)
                continue


    return list_of_ips


def read_any_file(file_path):

    file = Path(file_path).expanduser()
    
    if ( file.exists() ) :
        print(f"Reading from {str(file)}")
    else:
        print("File not found!!!\n")
        return -1

    if (file.suffix == ".json"):
        return read_json_file(file)
    elif (file.suffix == ".txt"):
        return read_txt_file(file)
    
# read_file("./ips.json")
# print(list_of_ips)
