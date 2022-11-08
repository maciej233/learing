from collections import namedtuple
import sys
import re
import os

"""
Program catch images from http response and save images from content
then it detects faces from images and save them either
"""


OUTDIR = '/home/maciej/learing/black_hat/sniffing_high/outputs'
PCAPS = '/home/maciej/learing/black_hat/sniffing_high/pcaps'
Response = namedtuple("Respone", ['header', 'payload'])

""" get header with Content-Type"""
def get_header(payload):
    try:
        raw_header = payload[:payload.index((b'\r\n\r\n')+2)]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None
    pattern = r'(?P<name>.*?): (?P<value>.*?)\r\n'
    header = dict(re.findall(pattern, raw_header.decode()))
    if 'Content-Type' not in header:
        return None
    return header

def extract_content(Response, content_name='image'):
    pass


class Reccaper:
    def __init__(self) -> None:
        pass
    """Get header from packet"""
    def get(self):
        pass
    """if there is image it write it down"""
    def write(self):
        pass

if __name__ == "__main__":
    file = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Reccaper(file)
    recapper.get()
    recapper.write('image')