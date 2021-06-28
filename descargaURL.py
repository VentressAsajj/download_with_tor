#!/usr/bin/python3
# -*- coding: utf-8 -*-
# by @nuria_imeq
'''
Analizo html de pagina C2 malware. Se procesa automaticamente.
'''

import json
import argparse
import requests
import sys
import codecs
import re
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup

# Configuracion de headers y url de descarga. Configura el user-agent para
# que sea Windows y no tengas problemas con la descarga, aunque puede poner
# el que quieras
url = 'URLdedescarga'
token = "pontutokenIPINFO"
headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}


def parserARGs():
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
        controller.authenticate(password='pontuclaveentor')
        controller.signal(Signal.NEWNYM)
        print("Success!! New Tor connection")

def downloadHTML():
    # python -m http.server
    session = testConnectTorIdentity()
    response = session.get(url, headers=headers)

    return response.text

def showInfoIP(ip):
    # consulta ipinfo = https://ipinfo.io/IP/json?token=pontutoken'
    # respuesta json {ip,city,region,county.loc,org,postal,timezone}
    # me quedo con country y lo transformo en code_country
    # loc tengo que pasearlo para crear coordenadas geoip
    # postal y timezone estas dos últimas por curiosidad
    url = "https://ipinfo.io/"+ip+"/json?token="+token
    print(url)
    session = testConnectTorIdentity()
    response = session.get(url)
    return json.loads(response.text)

def createJSON(timestamp,reg):
    dispositivo = reg[3].strip()
    source_ip = reg[4].strip()
    ciudad = reg[5].strip()
    ciudad.encode('utf-8')
    region = reg[6].strip()
    region.encode('utf-8')
    pais = reg[7].strip()
    pais.encode('utf-8')
    ipinfo = showInfoIP(source_ip)
    timezone = ipinfo['timezone']
    postal = ipinfo['postal']
    code_country = ipinfo['country']
    latitude,longitude = ipinfo['loc'].split(',')
    data_set = {
        'timestamp'   : timestamp,
        'timezone'    : timezone,
        'dispositivo' : dispositivo,
        'source_ip'   : source_ip,
        'city'        : ciudad,
        'postal'      : postal,
        'region'      : region,
        'latitude'    : latitude,
        'longitude'   : longitude,
        'location'    : {'lon':longitude, 'lat':latitude},
        'country'     : pais,
        'code_country':code_country
    }
    json_data = json.dumps(data_set, ensure_ascii=False)
    print(json_data)
    return json_data

def parseHTML(response,file):
    # el title contiene el total de ips que se han descargado el malware
    bs = BeautifulSoup(response, 'html.parser')
    cont_ips = (bs.html.body.title).string
    total_ips = bs.find_all(string=re.compile("#"))
    #print("IPs que han picado: ", cont_ips)

    # reg => cont # yy-mm-dd  #  hh:mm:ss # movil/pc # ip # ciudad # provincia # pais
    cont = 1
    json_data = {}
    f = open(file, 'w')
    for list in total_ips:
        reg = list.split("#")
        timestamp = reg[1]+"T"+reg[2]+"."+str(cont)+"Z"
        timestamp = timestamp.replace(" ","")
        cont += 1
        data_set = createJSON(timestamp,reg)
        f.write(data_set)
        f.write("\n")

    f.close()

def main():
    newTorIdentity()
    args = parserARGs()
    #print(args)
    if ( args.test is None ):
        session = testConnectTorIdentity()
        print(session.get("https://httpbin.org/get").text)
        sys.exit(2)
    else:
        # comento esto para no hacer ruido a los malosmalotes
        #response = downloadHTML()
        response = codecs.open("salida.html", "r", "utf-8").read()
        parseHTML(response,args.outputfile.name)



if __name__ == "__main__":
    main()
