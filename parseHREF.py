# -*- coding: utf-8 -*-
# by @nuria_imeq
'''
Descarga url con tor para obtener el tags <a href>
Dependencias:
    pip3 install stem requests bs4 requests[socks]

Ejecucion:
    python3 parseHREF.py url

IMPORTANTE - cambiar:
    PASS_TOR por la clave que has puesto en TOR
'''
import requests
import jsbeautifier
import sys
import json
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller

PASS_TOR = "CAMBIA"

def newTorIdentity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='PASS_TOR')
        controller.signal(Signal.NEWNYM)
        print("Success!! New Tor connection")

def ConnectTorIdentity():
    session = requests.session()
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

def parseURL(url):
    ip = url.split("/")[2]
    return ip

def main():
    data_set = {}
    url = str(sys.argv[1])
    ip = parseURL(url)
    f = open(ip + '.json', 'w')
    headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}
    newTorIdentity()
    session = ConnectTorIdentity()
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    for lnk in links:
        data_set = json.dumps({'href':lnk})
        f.write(data_set)
        f.write("\n")

if __name__ == "__main__":
    main()
