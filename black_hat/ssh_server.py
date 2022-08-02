"""Server side"""

from tkinter import EXCEPTION
import paramiko
import sys
import threading
import socket

class Server():
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'maciej' and password == 'password':
            return paramiko.AUTH_SUCCESSFUL

def main():
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = '2222'
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.bind((SERVER_IP, SERVER_PORT))
        connection.listen(100)
        print("******CONNECTING TO SERVER*******")
        client, address = connection.accept()
        print(f"You have connected to server {address[0]}:{address[1]}\n", client)
    except EXCEPTION as e:
        print(f"Exception occured {e}")
        sys.exit(1)
    



if __name__ == "__main__":
    main()