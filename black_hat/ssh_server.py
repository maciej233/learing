<<<<<<< HEAD
"""Server side"""


=======
import os
>>>>>>> 64d5800a2d285463c79efbc80dd91ece1abb70a5
import paramiko
import socket
import sys
import threading
<<<<<<< HEAD
import socket
import os

CWD = os.path.dirname(os.path.realpath(__file__))
RSA_KEY = paramiko.RSAKey(filename=os.path.join(CWD, "id_rsa_test"))
=======
>>>>>>> 64d5800a2d285463c79efbc80dd91ece1abb70a5

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, '.test_rsa.key'))


class Server (paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
<<<<<<< HEAD
        if (username == 'maciej') and (password == 'password'):
            return paramiko.AUTH_SUCCESSFUL

def main():
    SERVER_IP = '172.26.30.2'
    SERVER_PORT = 2222
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.bind((SERVER_IP, SERVER_PORT))
        connection.listen(100)
        print("******CONNECTING TO SERVER*******")
        client, address = connection.accept()
        print(f"\n\nYou have connected to server {address[0]}:{address[1]}", client)
    except Exception as e:
        print(f"Exception occured {e}")
        sys.exit(1)
    
    bhsession = paramiko.Transport(client)
    bhsession.add_server_key(RSA_KEY)
    server = Server()
    bhsession.start_server(server=server)

    chan = bhsession.accept(20)
    if chan is None:
        print("*** NO CHANNEL! ***")
        sys.exit(1)

    print("[+] AUTHENTICATED!")
    print(chan.recv(1024))
    chan.send("WELCOME TO BHSESSION")

    try:
        while True:
            command = input("Enter command: ")
            if command != "exit":
                chan.send(command)
                response = chan.recv(8192)
                print(response.decode())
            else:
                chan.send("exit")
                print("exiting")
                bhsession.close()
                break
    except KeyboardInterrupt:
        bhsession.close()    
    
if __name__ == "__main__":
    main()
=======
        if (username == 'tim') and (password == 'sekret'):
            return paramiko.AUTH_SUCCESSFUL


if __name__ == '__main__':
    server = '192.168.1.207'
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection ...')
        client, addr = sock.accept()
    except Exception as e:
        print('[-] Listen failed: ' + str(e))
        sys.exit(1)
    else:
        print(f'[+] Got a connection! from {addr}')

    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    chan = bhSession.accept(20)
    if chan is None:
        print('*** No channel.')
        sys.exit(1)

    print('[+] Authenticated!')
    print(chan.recv(1024).decode())
    chan.send('Welcome to bh_ssh')
    try:
        while True:
            command = input("Enter command: ")
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()
>>>>>>> 64d5800a2d285463c79efbc80dd91ece1abb70a5
