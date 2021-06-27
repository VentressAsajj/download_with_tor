#!/usr/bin/python3
# -*- coding: utf-8 -*-
# by @nuria_imeq
'''
Analizo la etiqueta <br> de la pagina que me descargo
'''

import json
import argparse
import requests
import sys
import codecs
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup

# Configuracion de headers y url de descarga. Configura el user-agent para
# que sea Windows y no tengas problemas con la descarga, aunque puede poner
# el que quieras
url = 'PON_URL_A_DESCARGAR'
headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}


def parser_args():
    parser = argparse.ArgumentParser(
            description = 'Descarga una pagina usando TOR como proxy',
            prog = 'descargaURL.py', usage='%(prog)s [-h]'
    )
    parser._optionals.title = "Opciones:"
    parser.add_argument("-f", "--outputfile", help="fichero de salida en formato json", nargs='?', type=argparse.FileType('w'), default=sys.stdin)
    parser.add_argument("-t", "--test", help="verifica la conexion con nodo tor", choices=["json"], nargs='?', default=sys.stdin)
    parser.add_argument("-v", "--verbose",   help="output verbose", action="store_true")
    parser.add_argument("-V", "--version", action='version', version='%(prog)s version 1.0')
    return parser.parse_args()


def testConnectTorIdentity():
    session = requests.session()
    # puedes cambiar esto por el privoxy
    #proxy = {'http': '127.0.0.1:8118'}
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

def newTorIdentity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='PON_LA_CALVE_EN_CLARO')
        controller.signal(Signal.NEWNYM)
        print("Success!! New Tor connection")

def downloadHTML():
    # python -m http.server
    session = testConnectTorIdentity()
    response = session.get(url, headers=headers)
    return response.text

def parseHTML(response):
    bs = BeautifulSoup(response, 'html.parser')
    print(bs.html.body.br)

def main():
    newTorIdentity()
    args = parser_args()
    #print(args)
    if ( args.test is None ):
        session = testConnectTorIdentity()
        print(session.get("https://httpbin.org/get").text)
        sys.exit(2)
    else:
        # comento esto para no hacer ruido a los malosmalotes
        #response = downloadHTML()
        response = codecs.open("salida.html", "r", "utf-8").read()
        parseHTML(response)


if __name__ == "__main__":
    main()
