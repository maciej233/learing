import socket
import sys

IP = "127.0.0.1"
PORT = 9800

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection.connect((IP, PORT))

with open("test.txt", 'r') as f:
    text = f.read().encode("UTF-8")

    connection.send(text)

    output = connection.recv(1024)

    print(output.decode())

    connection.close()
