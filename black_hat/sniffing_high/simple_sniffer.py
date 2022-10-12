from scapy.all import *

def call_back(packet):
    print(packet.show())

sniff(filter="", prn=call_back, store=0, count=1)
