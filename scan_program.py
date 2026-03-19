import subprocess


def fast_scan(command):
    result = subprocess.run("masscan 172.18.27.233/20 -p22 -oL -", capture_output=True, text=True, shell=True)

    
    return result


result = fast_scan("")

print(result.stdout)
