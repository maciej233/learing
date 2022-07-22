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
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # avoid error message what address is in use (wait)
        
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
    # funckja obsługująca wysyłanie wiadomości client<=>server
    def send(self):
        self.socket.connect((self.args.target, self.args.port)) # nawiąż połaczenie z serwerem IP:PORT
        if self.buffer: # sprawdza czy jest cos w sys.stdin.read()
            self.socket.send(self.buffer) # wysyła zapytanie na server

        try:
            while True:
                respone = ''
                recv_len = 1
                while recv_len: # sprawdza czy jest odpowiedz
                    data = self.socket.recv(4096) # pobiera odpowiedz z servera do 4096 bitów
                    respone += data.decode() # zmieniamy na string czytelny dla użytkownika
                    recv_len = len(data)
                    if recv_len < 4096: # jeśli zmieścilimsy się w buforze i wszystko zostało pobrane przerywa pętle
                        break
                if respone: # sprawdzamy czy coś przyszło z servera do clienta
                    print(respone) # odczytjemy odpowiedz juz w postaci decode()
                    buffer = input("> ") # zmianiamy/czyscimy buffor na prompt >
                    buffer += '\n' 
                    self.socket.send(buffer.encode()) # wysyłamy potwierdzeniew bitach na server
        except KeyboardInterrupt:
            print("CONNECTION CLOSE BY USER")
            self.socket.close()
            sys.exit()        
    # funkcja uruchamiana na serwerze w celu nasłuchiwania zapytań
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))  # tworzy socket nasłuchujący dla servera
        self.socket.listen(5) # przyjmuje do pięciu połączeń w tym samym czasie
        while True:
            client_socket, _ = self.socket.accept() # po akceptacji zapytania nas server zwraca nam clienta, adres[0]=IP, adres[1]=PORT
            client_thread = threading.Thread(target=self.handler, args=(client_socket,)) # tworzy obsługę kilku zapytań na server, na tym samym CPU
            client_thread.start() # uruchamiamy funckę handler
    # tworzy osbługę zapytań na server, a dokładnie 3 moetod --command, --execute, --upload okreśłonych w main()
    def handler(self, client_socket):

        if self.args.execute: # jeśli zapytanie było -e lub --execute
            output = execute(self.args.execute) # przysyła zapytanie na server np "ls -la"
            client_socket.send(output.encode())
        # jeśli chcemy uruchmić shell w celu wpisania wielu commend zamiant pojedyńczej jak w przypadku --execute
        elif self.args.command:
            cmd_buffer = b'' # tworzymy pusty buffer w którym zapiszemy nasze komendy np echo "HELLO"
            while True:
                try:
                    client_socket.send(b'BHP:# ') # powinien nam się uruchomić na cliencie nowy prompt do wpisywania commmend
                    while '\n' not in cmd_buffer.decode(): # zbiera całą komendę zanim naciśniemy enter
                        cmd_buffer +=client_socket.recv(64)
                    response = execute(cmd_buffer.decode()) # wykonaj komendę znalezioną w buforze i zwróć zapytanie z servera
                    if response: # jesli jakaś comenda się wykona
                        client_socket.send(response.encode()) # PKOAŻ u clienta odpowiedz w postaci stringa
                    cmd_buffer = b'' # czyścimy buffor i powtarzmy, aż nie przerwiamy np poprzez Ctr+C
                except Exception as e:
                    print(f"server killed {e}")
                    self.socket.close()
                    sys.exit()
        # funkcja pomoncnicza do obłusgi commendy --upload
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, "wb") as f:
                f.write(file_buffer)
            message = f"you have succesfull write to file {self.args.upload}"
            client_socket.send(message.encode()) # zwróc zapytanie do clienta w postaci stringa

# main function
def main():
    parser = argparse.ArgumentParser(description="Your personal nc program",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""Exaples:                                    
        netcat.py -t 192.168.0.1 -p 5555 -l -c              # command shell
        netcat.py -t 192.168.0.1 -p 5555 -l -u=myfile.txt   # upload file
        netcat.py -t 192.168.0.1 -p 5555 -l -e              # execute one command
        netcat.py -t 192.168.0.1 -p 5555                    # connect to server
        """))

    parser.add_argument("-e", "--execute",                          help="execute command")
    parser.add_argument('-l', '--listen',   action="store_true",    help="listen on port")
    parser.add_argument('-c', '--command',  action="store_true",    help="command shell")
    parser.add_argument('-t', '--target',   default="127.0.0.1",    help="target IP")
    parser.add_argument('-p', '--port',     default=5555, type=int, help="target port")
    parser.add_argument('-u', '--upload',                           help="upload file")
    
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()


# funkcja pomoncnicza do obłusgi commendy --execute
def execute(cmd):
    cmd=str(cmd)
    cmd.strip()
    if not cmd:
        return
    else:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

if __name__ == "__main__":
    main()
