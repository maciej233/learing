from ctypes import Structure, c_ubyte, c_uint, c_ushort
import socket
import struct

"""
c_ubyte unsigned char
c_ushort unsigned  short
c_ubyte unsigned intetger
"""
class IP(Structure):
    __fields__ = [
        ("version", c_ubyte, 4),
        ("hdr", c_ubyte, 4),
        ("tos", c_ubyte, 8),
        ("length",  c_ushort, 16),
        ("id", c_ushort, 16),
        ("offset", c_ushort, 16),
        ("ttl", c_ubyte, 8),
        ("proto", c_ubyte, 8),
        ("checksum", c_ushort, 16),
        ("src", c_uint, 32),
        ("dst", c_ubyte, 32)
    ]
    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.src_address = socket.inet_ntoa(struct.pack("L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("L", self.dst))
