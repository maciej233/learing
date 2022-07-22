"""Program will mimics the netcat 'nc' framework"""
import argparse
import threading
import sys
import textwrap
import subprocess
import shlex
import socket

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                respone = ''
                recv_len = 1
                while recv_len:
                    data = self.socket.recv(4096)
                    respone += data.decode()
                    recv_len = len(data)
                    if recv_len < 4096:
                        break
                if respone:
                    print(respone)
                    buffer = input("> ")
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("CONNECTION CLOSE BY USER")
            self.socket.close()
            sys.exit()        

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handler, args=(client_socket,))
            client_thread.start()

    def handler(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #>')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer +=client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f"server killed {e}")
                    self.socket.close()
                    sys.exit()

        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.arga.upload, "wb") as f:
                f.write(file_buffer)
            message = f"you have succesfull write to file {self.args.upload}"
            client_socket.send(message.encode())

# main function
def main():
    parser = argparse.ArgumentParser(description="Your personal nc program",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""Exaples:                                    
        netcat.py -t 192.168.0.1 -p 5555 -l -c          # command shell
        netcat.py -t 192.168.0.1 -p 5555 -u file.txt    # upload to file ./file.txt
        netcat.py -t 192.168.0.1 -l  ...
        """))

    parser.add_argument("-e", "--execute", action="store_true", help="execute command")
    parser.add_argument('-l', '--listen', help="listen on port")
    parser.add_argument('-c', '--command', action="store_true", help="command shell")
    parser.add_argument('-t', '--target',default="127.0.0.1", help="target IP")
    parser.add_argument('-p', '--port', type=int, default=5555, help="target port")
    parser.add_argument('-u', '--upload', help="upload file")
    
    args = parser.parse_args()

    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()


def execute(command):
    command.strip()
    if not command:
        return
    else:
        output = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)        
    return output.decode()

if __name__ == "__main__":
    main()