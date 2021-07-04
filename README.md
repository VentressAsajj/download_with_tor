Para más documentación visitia la wiki<p>

## Instalación.
Instala los modulos pyhton del programa.
Por ahora no tengo fichero requirements.txt lo haré, mientras tanto puedes hacer:

```
  git clone https://github.com/VentressAsajj/download_with_tor.git
  cd download_with_tor
  pip3 install stem requests bs4 requests[socks]
```
Tienes una ayuda:
```
  python3 descargaURL.py -h
    usage: descargaURL.py [-h]

    Descarga una pagina usando TOR como proxy

    Opciones::
      -h, --help            show this help message and exit
      -o [OUTPUTFILE], --outputfile [OUTPUTFILE]
                            fichero de salida en formato json
      -i [INPUTFILE], --inputfile [INPUTFILE]
                            fichero de entrada en formato html
      -u URL, --url URL     url para descargar
      -d DOMAIN_MALWARE, --domain_malware DOMAIN_MALWARE
                            dominio malware
      -t [TEST], --test [TEST]
                            verifica la conexion con nodo tor
      -v, --verbose         output verbose
      -V, --version         show program's version number and exit

```
Puedes pasarle el dominio del la url para que quede como campo en el fichero json.<p>
Puedes pasar la url para descargar el fichero html o indicar ese fichero como argumento de entrada, en formato html.<p>
Indica siempre un fichero de salida.<p>
Puedes realizar un test para ver si te funciona la red TOR.<p>

## Roadmap
- [x] Configuración tor y privoxy<p>
- [x] Descarga url desde tor buscando anonimato<p>
- [x] Analisis/parse html con modulo beautifulSoup<p>
  - [x] Generar el objeto json del parse del html<p>
  - [x] timestamp en el json<p>
- [x] Generar fichero json con resultado<p>
- [x] ¿Cargar json desde programa o desde logstash? se admite sugerencias<p>
- [x] Consulta por IP en ipinfo.io para obtener el ASN 
- [-] Añadir como argumento de entrada la url. Descartado<p>
- [-] Posibiliad que lea fichero html como argumento de entradar. Descartado<p>
- [X] Añadir como argumento el dominio.<p>
- [X] Añadir marca de tiempo en el fichero de salida.<p>
- [ ] Registro de actividad. Creación de log.<p>
- [ ] Analizando el phishing publicado en tw.
- [ ] Mirar modulo torpy[request] por si merece la pena.


Last update  dom 04 jul 2021 11:56:25 CEST
