from ctypes import Structure, c_ubyte, c_uint, c_ushort
import socket
import struct
import os
import sys
import ipaddress

"""
c_ubyte unsigned char
c_ushort unsigned  short
c_ubyte unsigned intetger
"""


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
        self.src_address = socket.inet_ntoa(struct.pack("L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("L", self.dst))
        self.protocal_map = {1: "ICMP", 6:"TCP", 17: "UDP"}
        try:
            self.protocol = self.protocal_map[self.protocol_num]
        except Exception as e:
            print("%s \nNO protocl for %s") % (e, self.protocl_num)
            self.protocol = str(self.protocol_num)


def sniff(host):
    if os.name == "nt":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            ip_header = IP(raw_buffer)[0:20]
            print("Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
    
    except KeyboardInterrupt:
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = "192.168.8.100"
    sniff(host)





