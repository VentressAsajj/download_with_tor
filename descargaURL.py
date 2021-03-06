# -*- coding: utf-8 -*-
# by @nuria_imeq
'''
Descarga url con tor.
El parse del html es algo especial, es un C2.
Argumentos obligados, url y domain_malware, domain_malware es obligatorio porque
lo uso, junto con la ip, para quitarme eventos duplicados. Se realiza el fingerprint de ambos.
El fingerprint lo hago el logstash. Si no quieres que sea requerido quita required=True

IMPORTANTE - cambiar:
    URL por la url que deseas descargar
    TOKEN_IPINFO por el token de ipinfo
    PASS_TOR por la clave que has puesto en TOR

Dependencias:
    pip3 install stem requests bs4 requests[socks]

Ejecucion:
    python3 descargaURL.py [ARGS]

Ayuda:
    python3 descargaURL.py -h
'''

import json
import argparse
import requests
import sys
import codecs
import re
from datetime import datetime
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup

# Configuracion de headers y url de descarga. Configura el user-agent para
# que sea Windows y no tengas problemas con la descarga, aunque puede poner
# el que quieras
url = 'http://URL'
token = "TOKEN_IPINFO"
headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}


def parserARGs():
    parser = argparse.ArgumentParser(
            description = 'Descarga una pagina usando TOR como proxy',
            prog = 'descargaURL.py', usage='%(prog)s [-h]'
    )
    parser._optionals.title = "Opciones:"
    parser.add_argument("-o", "--outputfile", help="fichero de salida en formato json", nargs='?', type=argparse.FileType('w'), default="salida.json")
    parser.add_argument("-d", "--domain_malware", help="dominio malware")
    parser.add_argument("-t", "--test", help="verifica la conexion con nodo tor", nargs='?', default=sys.stdin)
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
        controller.authenticate(password='PASS_TOR')
        controller.signal(Signal.NEWNYM)
        print("Success!! New Tor connection")

def downloadHTML():
    # python -m http.server
    session = testConnectTorIdentity()
    response = session.get(url, headers=headers)
    return response.text

def currentDate(date):
    day   = date.day
    month = date.month
    year  = date.year
    hour  = date.hour
    min   = date.minute
    seg   = date.second
    now = "{}-{}-{}_{}{}{}".format(year,month,day,hour,min,seg)
    return now

def showInfoIP(ip):
    # consulta ipinfo = https://ipinfo.io/IP/json?token=pontutoken'
    # respuesta json {ip,city,region,county.loc,org,postal,timezone}
    # me quedo con country y lo transformo en code_country
    # loc tengo que pasearlo para crear coordenadas geoip
    # postal y timezone estas dos ??ltimas por curiosidad
    url = "https://ipinfo.io/"+ip+"/json?token="+token
    print(url)
    session = testConnectTorIdentity()
    response = session.get(url)
    return json.loads(response.text)

def createJSON(timestamp,reg,domain):
    data_set={}
    dispositivo = reg[3].strip()
    source_ip = reg[4].strip()
    ciudad = (reg[5].strip())
    region = (reg[6].strip())
    pais = (reg[7].strip())
    ipinfo = showInfoIP(source_ip)
    timezone = ipinfo['timezone']
    postal = ipinfo['postal']
    code_country = ipinfo['country']
    asn= ipinfo['org']
    latitude,longitude = ipinfo['loc'].split(',')
    data_set = {
        'timestamp'     : timestamp,
        'timezone'      : timezone,
        'dispositivo'   : dispositivo,
        'source_ip'     : source_ip,
        'city'          : ciudad,
        'postal'        : postal,
        'region'        : region,
        'latitude'      : latitude,
        'asn'           : asn,
        'longitude'     : longitude,
        'location'      : {'lon':longitude, 'lat':latitude},
        'country'       : pais,
        'domain_malware': domain,
        'code_country'  :code_country
    }
    json_data = json.dumps(data_set, ensure_ascii=False)
    print(json_data)
    return json_data

def parseHTML(response,file,domain):
    # el title contiene el total de ips que se han descargado el malware
    bs = BeautifulSoup(response, 'html.parser')
    cont_ips = (bs.html.body.title).string
    total_ips = bs.find_all(string=re.compile("#"))

    # reg => cont # yy-mm-dd  #  hh:mm:ss # movil/pc # ip # ciudad # provincia # pais
    cont = 000
    json_data = {}
    now = currentDate(datetime.now())
    file = file + "_" + now
    f = open(file, 'w')
    for list in total_ips:
        reg = list.split("#")
        timestamp = reg[1]+"T"+reg[2]+"."+str(cont)+"Z"
        timestamp = timestamp.replace(" ","")
        data_set = createJSON(timestamp,reg,domain)
        f.write(data_set)
        f.write("\n")

    f.close()

def main():
    args = parserARGs()
    #print(args)
    newTorIdentity()
    if ( args.test is None ):
        session = testConnectTorIdentity()
        print(session.get("https://httpbin.org/get").text)
        sys.exit(2)


    # puedes hacer una carga de un html, solo descomenta esta linea y comenta la siguiente
    response = codecs.open("entrada.html", "r", "utf-8").read()
    # # comento esto para no hacer ruido a los malosmalotes
    #response = downloadHTML()
    if ( args.domain_malware is None):
        print ("El dominio de malware debe ser especificado")
        sys.exit(2)
        
    parseHTML(response, args.outputfile.name, args.domain_malware)

if __name__ == "__main__":
    main()
