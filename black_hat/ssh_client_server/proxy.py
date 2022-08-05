"""
   The program derived from book black hat python
   By Justin Seitz and Tim Arnold
   This is proxy server to sniff data go through client-server
   like ftp server
"""
import sys
import socket
import threading

FILTER = ''.join(len(repr(chr(i))) == 3 and chr(i) or '.' for i in range(256))

# Display communication beetwen remote machince and local to the console
def hexdump(src, length=10, show=True):
    if isinstance(src, bytes): # make sure the input is a string, ints will crush program bcs of ord() function
        src = src.decode()
    output = []
    for i in range(0, len(src), length):
        word = str(src[i:i+length]) # we cut the sensence in pices with parametr length
        printable = word.translate(FILTER) # make printable representation of all characters supported by ASCII
        hex = ' '.join([f'{ord(letter):02X}'for letter in word]) # change every letter in "piece of sentace"= "word" to hex
        hexwidth= length*3 # just for nice show up
        output.append(f'{i:04X} {hex:<{hexwidth}} {printable}') #put all together in the list
    if show:
        for line in output:
            print(line)
    else:
        return output

# receive communication from either local and remote machine to server
def recevie_from(connection):
    buffer = b''
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer

# manage traffic directions beetwen remote and local machine
def proxy_handler(client_sokcet, remote_ip, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_ip, remote_port))

    if receive_first:
        remote_buffer = recevie_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print('<=== sending %d bytes to localhost' % len(remote_buffer))
        client_sokcet.send(remote_buffer)

    while True:
        local_buffer = recevie_from(client_sokcet)
        if len(local_buffer):
            print('<=== we received %d from localhost' % len(local_buffer))
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)

        remote_buffer = recevie_from(remote_socket)
        if len(remote_buffer):
            print("we received %d from remote" % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_sokcet.send(remote_buffer)

        if not len(local_buffer) or not len(remote_buffer):
            client_sokcet.close()
            remote_socket.close()
            print("connection closed")
            break     


# listening socket on server which pass data to proxy_hanlder
def server_loop(server_ip, server_port, remote_ip, remote_port, recevie_first):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((server_ip, server_port))
    except Exception as e:
        print(f"Failed to lisnintg on server {server_ip} because of {e}")
        print("Check firewall configuration and try again")
        sys.exit(0)

    print(f"**** Listening on {server_ip}:{server_port}")
    server_socket.listen(5)
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"recevied connection from {client_address[0]}:{client_address[1]}")
        
        client_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_ip, remote_port, recevie_first))
        client_thread.start()

# modify the request - authentication issue, icmp etc..
def request_handler(buffer):
    return buffer

# modify the response
def response_handler(buffer):
    return buffer

def main():
    if len(sys.argv[1:]) != 5:
        print("Example usage:\n ~/learing/black_hat/proxy.py 127.0.0.1 5000 172.26.2.10 5000 False")
        sys.exit(0)
    client_ip = sys.argv[1]
    client_port = int(sys.argv[2])
    remote_ip = sys.argv[3]
    remote_port = int(sys.argv[4])
    recevice_first = sys.argv[5]

    if recevice_first == "True":
        recevice_first = "True"
    else:
        recevice_first = "False"

    server_loop(client_ip, client_port, remote_ip, remote_port, recevice_first)

if __name__ == "__main__":
    main()
