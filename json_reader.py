import json as json

list_of_hosts = []
list_of_ips   = []

def read_file(file_name):

    global list_of_ips, list_of_hosts

    file = open(file_name)

    if(file == None):
        print("File does not exit!!!")
        return -1
    print("File Opened Successfully")

    list_of_hosts = json.load(file)

    #print(list_of_hosts)


    for element in list_of_hosts:
        print(str(element.get("ip")))

        list_of_ips.append( str( element.get("ip")))


    return list_of_ips
# read_file("./ips.json")
# print(list_of_ips)
