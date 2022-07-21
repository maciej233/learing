"""This program mimics NetCat Framework"""

import socket
import subprocess
import shlex
import argparse
import textwrap
import sys


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
            respone = ''
            receive = 1
            while receive:
                break

        except KeyboardInterrupt:
            print("User terminated")
            self.socket.close()
            sys.exit(0)


    def listen(self):
        pass



"""Executable command write in command line"""
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output

"""Create the command line interface for user"""
def main():
    parser = argparse.ArgumentParser(description="Your personal Netcat Interface",
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    epilog=textwrap.dedent("""Examples:
                                    netcat -p 9990 -w 5 -t 192.168.0.1 42 # open tcp session on dport 42 sport 9990 on host 192.168.0.1 with timeout 5 seconds
                                    netcat -t 192.168.0.1 -p 5555 -l -c # command shell
                                    netcat -t 192.168.0.1 -p 9990 -l -u=myfile.txt # upload output to file
                                    netcat -t 192.168.0.1 -p 9990 -e=\cat /etc/passwd" # run command
                                    echo 'text' | ./netcat.py -t 192.168.0.1 -p 1300 # send 'text' to server on port 1300             
                                    """)
                                    )

    parser.add_argument("-l", "--listen", action="store_true", help="Listing on port")
    parser.add_argument("-c", "--command", action="store_true", help="command shell")
    parser.add_argument("-p", "--port", type=int, default=5555, help="port")
    parser.add_argument("-t", "--target", default="127.0.0.1", help="Target IP address")
    parser.add_argument("-e", "--execute", help="execute specific command")
    parser.add_argument("-u", "--upload", default="./output.txt", help="Upload outpul to file")

    args = parser.parse_args()

    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()

    

if __name__ == "__main__":
    main()
    
