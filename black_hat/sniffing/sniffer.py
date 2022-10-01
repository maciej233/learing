"""Program decode the IP header from packet without option field"""
from ctypes import Structure, c_ubyte, c_uint, c_ushort
import socket
import struct
import os
import sys


"""Create the structure of IP packet
c_ubyte unsigned char
c_ushort unsigned  short
c_ubyte unsigned intetger
"""

OS_NAME = "nt"  # nt for windows


class IP(Structure):
    __fields__ = [
        ("ver", c_ubyte, 4),
        ("hdr", c_ubyte, 4),
        ("tos", c_ubyte, 8),
        ("length",  c_ushort, 16),
        ("id", c_ushort, 16),
        ("offset", c_ushort, 16),
        ("ttl", c_ubyte, 8),
        ("protocol_num", c_ubyte, 8),
        ("checksum", c_ushort, 16),
        ("src", c_uint, 32),
        ("dst", c_ubyte, 32)
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

class ICMP(Structure):
    pass


def sniff(host):
    if os.name == OS_NAME:
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol) # raw socket
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)  # include IP headers

    if os.name == OS_NAME:
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON) # promisous mode for windows

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0] # catch first packet
            ip_header = IP(raw_buffer)[0:20] # create IP header object
            print("Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)) # pull out protocol src and dest from packet
    
    except KeyboardInterrupt:
        if os.name == OS_NAME:
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF) # trun of prmiscous mode
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = "192.168.1.173"
    sniff(host)