from collections import namedtuple
from scapy.all import rdpcap, TCP
import sys
import re
import os
import zlib

"""
Program catch images from http response and save images from content
then it detects faces from images and save them either
"""


OUTDIR = '/home/maciej/learing/black_hat/sniffing_high/face_detector/pictures'
PCAPS = '/home/maciej/learing/black_hat/sniffing_high/face_detector/pcaps'
Response = namedtuple("Respone", ['header', 'payload'])

""" get header with Content-Type"""
def get_header(payload):
    try:
        raw_header = payload[:payload.index(b'\r\n\r\n')+2]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None
    pattern = r'(?P<name>.*?): (?P<value>.*?)\r\n'
    header = dict(re.findall(pattern, raw_header.decode()))
    if 'Content-Type' not in header:
        return None
    return header

"""Get images from payload based on headers"""
def extract_content(Response, content_name='image'):
    content, content_type = None, None
    if content_name in Response.header['Content-Type']:  # check if there is image in payload looking on header
        content_type = Response.header['Content-Type'].split('/')[1]  # for example image/png or image/jpg check type of image
        content = Response.payload[Response.payload.index(b'\r\n\r\n')+4:]

        if 'Counter-Encoding' in Response.header:
            if Response.header['Counter-Encoding'] == 'gzip':
                content = zlib.decompress(Response.payload, zlib.MAX_WBITS | 32 )
            if Response.header['Counter-Encoding'] == 'deflate':
                content = zlib.decompress(Response.payload)
    return content, content_type


class Reccaper:
    def __init__(self, file_name) -> None:
        pcap = rdpcap(file_name)  # create object of file we want to read
        self.session = pcap.sessions() # seperate tcp seasion
        self.responses = list()
    """Traverse packets to get seperate Response from pcap file"""
    def get(self):
        for session in self.session:
            payload = b''
            for packet in self.session[session]:
                try:
                    if packet[TCP].dport == 443 or packet[TCP].sport == 443:
                        payload += bytes(packet[TCP].payload)
                except IndexError:
                    sys.stdout.write('X')
                    sys.stdout.flush()
            if payload:
                header = get_header(payload)
                if header is None:
                    continue
                self.responses.append(Response(header=header, payload=payload))
                    
    """iterate over the responses and write images to files"""
    def write(self, content_name):
        for i, response in enumerate(self.responses):
            content, content_type = extract_content(response, content_name)
            if content and content_type:
                file_name = os.path.join(OUTDIR, f'ex_{i}.{content_type}')
                print(f"Writing {file_name}")
                with open(file_name, 'wb') as file:
                    file.write(content)


if __name__ == "__main__":
    file = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Reccaper(file)
    recapper.get()
    recapper.write('image')