"""Program decode the IP header"""
from ctypes import Structure, c_ubyte, c_uint, c_ushort
import socket
import struct
import os
import sys
import ipaddress
import threading
from time import sleep
from threading import Thread

SUBNET = "172.26.30.0/24"
OS_NAME = "nt"  # nt for windows
MESSAGE = "MYMESSAGE"

"""Create the structure of IP packet
c_ubyte unsigned char
c_ushort unsigned  short
c_ubint unsigned intetger
< little endian
L unsigned long integer
B unsigned char integer
H unsigend_short integer
"""

"""Send UDP message to all hosts in subnet"""
def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sleep(1)
            sender.sendto(bytes(MESSAGE, "utf8"), (str(ip), 65212))

"""How to use ctypes in bytes operations
class IP(Structure):
    _fields_ = [
        ("ver", c_ubyte, 4),
        ("ihl", c_ubyte, 4),
        ("tos", c_ubyte, 8),
        ("length",  c_ushort, 16),
        ("id", c_ushort, 16),
        ("offset", c_ushort, 16),
        ("ttl", c_ubyte, 8),
        ("protocol_num", c_ubyte, 8),
        ("checksum", c_ushort, 16),
        ("src", c_uint, 32),
        ("dst", c_uint, 32)
    ]
    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # convert to readeable option
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        self.protocal_map = {1: "ICMP", 6:"TCP", 17: "UDP"}
        try:
            self.protocol = self.protocal_map[self.protocol_num]
        except Exception as e:
            print("%s \nNO protocl for %s") % (e, self.protocl_num)
            self.protocol = str(self.protocol_num)
"""
class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF
    
        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # human readable IP addresses
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # map protocol constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s No protocol for %s' % (e, self.protocol_num))
            self.protocol = str(self.protocol_num)

"""How to use struct in bytes operations"""
class ICMP:
    def __init__(self, buffer):
        header = struct.unpack("<BBHHH", buffer)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

"""Main function"""
class SNIFFER:
    def __init__(self, host):
        self.host = host
        if os.name == OS_NAME:
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)  # include IP headers
        print("hitting promiscous mode... ")
        if os.name == OS_NAME:
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON) # promisous mode for windows


    def sniff(self):
        hosts_up = set([f"{str(self.host)}*"])
        try:
            while True:
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[0:20])
                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl*4
                    buffer = raw_buffer[offset:offset+8]
                    icmp_header = ICMP(buffer)
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(SUBNET):
                            if raw_buffer[len(raw_buffer) - len(MESSAGE): ] == bytes(MESSAGE, "utf8"):
                                tgt = str(ip_header.src_address)
                                if tgt != self.host and tgt not in hosts_up:
                                    hosts_up.add(str(ip_header.src_address))
                                    print(f"Hosts Up: {tgt}")
        except KeyboardInterrupt:
            if os.name == OS_NAME:
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF) # trun off prmiscous mode
            print("\nUser interupted")
            if hosts_up:
                print(f"\n\nSummary: Hosts up on {SUBNET}")
            for host in sorted(hosts_up):
                print(f"{host}\n")
            sys.exit()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = "172.26.30.2"
    s = SNIFFER(host)
    sleep(5)
    t = threading.Thread(target=udp_sender)
    t.start()
    s.sniff()
    