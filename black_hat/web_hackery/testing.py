import urllib.request
import urllib.parse

url = "https://www.google.com"

"""------------------1---------------------------
simple get with urlop.request


with urllib.request.urlopen(url) as respone: # GET
    output = respone.read()

print(output)
"""


"""------------------2-------------------------------
simple post reqest wikth urlib.request

info = {"username": "NAME", "passoword":"PASS"}
data = urllib.parse.urlencode(info).encode()

req = urllib.request.Request(url, data)

with urllib.request.urlopen(req) as response: # POST
    output = response.read()
"""


"""---------------------3-----------------------
Time for requests library
import requests
info = {"username": "NAME", "passoword":"PASS"}
respone1 = requests.get(url=url) # GET
response2 = requests.post(url, data=info) # post
print(response2.text) # string
print(response2.content) # bytes
"""

"""having a HTML content we will retrive the content and parse the links from it"""

import requests
from io import BytesIO
from lxml import etree

url = 'https://nostarch.com'
r = requests.get(url)
content = r.content

parser = etree.HTMLParser()
content = etree.parse(BytesIO(content), parser=parser)
for link in content.findall('//a'):
    print(f"{link.get('href')} -> {link.text}")