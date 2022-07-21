import socket
import threading

IP = "127.0.0.1"
PORT = 9800


def main():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind((IP, PORT))
    connection.listen(5)
    print("******CONNECTING TO SERVER*******")
    while True:
        client, address = connection.accept()
        print(f"You have connected to server {address[0]}:{address[1]}")
        client_handler = threading.Thread(target=handler_client, args=(client,))
        client_handler.start()


# Helper Functions
def handler_client(client_socket):
    with client_socket as sock:
        request = sock.recv(4096)
        print(request.decode("UTF-8"))
        sock.send(b"ACK")


if __name__ == "__main__":
    main()
