import paramiko
import os

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def connect_to_vps(ip_address, username, key_path=None, password=None):
    # print(ip_address, username, password)
    
    try :
        client.connect(
            hostname=ip_address,
            username=username,
            key_filename=key_path,
            password=password,
            port=22
        )
    except Exception as e:
        print(f"Failed to connect to VPS: {e}")
        return False
    return True

 
def run(command):
    _, stdout, stderr = client.exec_command(command)
    return stdout.read().decode().strip()
 
# print(run("df -h /"))                        # disk usage
# print(run("free -m"))                        # memory
# print(run("systemctl is-active nginx"))      # nginx status
def usage(server, args):
    # print('Entering usage function')
    connection_flag = connect_to_vps(server["ip_address"], server["username"], password=args.password)
    result = {}

    if connection_flag:
        result["disk_usage"] = run("df -h /")  # disk usage
        result["memory_usage"] = run("free -m | awk 'NR==2{printf \"%s/%sMB (%.2f%%)\", $3,$2,$3*100/$2 }'")  # memory usage
        nginx_status = run("systemctl is-active nginx")  # nginx status
        result["nginx_status"] = "running" if nginx_status == "active" else "stopped"
        client.close()
        return result   
 