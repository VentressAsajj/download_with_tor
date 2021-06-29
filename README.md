# Descarga de url usando privoxy con tor

## Instalación y configuración de TOR y privoxy
```bash
apt-get install tor tor-geoipdb privoxy
```

## Configurando TOR
```bash
tor --hash-password passhere 
```
En el párrafo anterior hemos generado un hash de la clave ( passhere ) el cual lo debemos indicar en el fichero de configuración de tor.<p>
Copia el hash generado en el fichero **/etc/tor/torrc** y activa la autenticación en tor ( socks5 )
```bash
ControlPort 9051
HashedControlPassword generatedhash
```

## Configura privoxy:
Añade las siguientes lineas en el fichero de configuración de privoxy **/etc/privoxy/config**<p>
```bash
forward-socks5t   /               127.0.0.1:9050 .
listen-address  127.0.0.1:8118
``` 
Las siguientes lineas son opcionales<p>
```bash
keep-alive-timeout 600
default-server-timeout 600
socket-timeout 600
```
Reiniciamos servicios
```bash
service tor restart
service privoxy restart
```

## Test 
Comprueba que funciona el proxy y tor. Ejecuta los siguientes comandos. El primero te dará tu IP pública, el segundo la
ip del nodo de salida de tor, última te dará lo mismo que la anterior pero realizando la petición a través de el proxy (privoxy).    
```bash
curl http://ifconfig.me 
torify curl http://ifconfig.me
curl -x 127.0.0.1:8118 https://ifconfig.me
```
<p>
## Introducción
Bueno sinceramente aún no tengo claro si lo hago con privoxy o solo con tor.<p>
La idea surge a la hora de monitorizar la url donde aparecen las ips que han descargado el malware, el C2.<p>
En principio la descarga la hacía con un simple curl y proxychains, me descargaba el html, lo limpiaba, quedándome solo las ips para luego subirlas
a elasticsearch. Como soy vaga, quiero monitorizar este proceso, descargando la página en formato json. Dejándolo limpio para que pueda cargarlo
con logstash, intentando no perder la fecha del evento y otros datos que son muy interesantes.<p>
Además si cargo los eventos en elastic, y realizando la consulta para obtener el ASN de las IPs, podré generar alertas para instituciones
que son "delicadas".
La generación de ficheros se hace con un cron cada 5'.    

No me gusta borrar los comentarios anteriores porque muestran cómo evolucionan en el tiempo las pequeñas ideas o proyectos.
Voy a intentar resumirlo y no cambiar mucho el resumen.<p>
La idea surge cuando descubres el C2 de los malosmalotes, que son muy poco originales, y te van cambiando el dominio de 
descarga del malware pero poco más. <p>
Así llevamos desde Abril. Tanto @iso1600_net como yo hemos ido analizando el phishing, descargando los ficheros con malware, <p>
analizandolos, por cierto pocos antivirus lo detectan, hasta que un día encontramos la url de C2. Desde entonces han reutilizado<p>
la infraestructura para nuevas campañas y comprando nuevos dominios.<p>
Los paises afectados, España y Mexico. Que no sepa. <p>
Realize un proceso automatico de descarga, todo en bash y en el cron. Ahora he decidido usar python y realizar la ingesta en elastic.<p>


Realiza la descarga de una url, o carga un fichero en formato html. Parsea el fichero, el parse está muy adaptado al fichero de C2.<p>
Genera un json con los datos para cargarlos en elastic. <p>
El fichero de configuración de logstash realiza un fingerprint de la IP. Cuando hice la primera ingesta vi que había IPs repetidas,<p>
esto era debido a que el proceso se ejecutaba cada 5' y los registros del fichero, afortunadamente, no variaban mucho. Para evitar<p>
eventos duplicados, he realizado un fingerprint de la IP y lo he vinculado con el id del documento.

El reto ahora es seguir analizando el phishing publicado en tw.

## Instalación.
Instala los modulos pyhton del programa. A estas alturas deberías saber cómo se instalan, quizá haga un fichero requirements.txt <p>
para hacerlo de forma automática. Tira de:
```
git clone https://github.com/VentressAsajj/download_with_tor.git
cd download_with_tor
chmod +x descargaURL.py 
pip3 install json argparse requests codecs re BeautifulSoup stem
```
No estoy muy segura porque ya tenía modulos instalados, venga prometo hacerlo bien :D
Tienes una ayuda:
```
./descargaURL.py -h
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
Puedes pasar la url para descargar el fichero html o indicar ese fichero como argumento de entrada.<p>
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
- [X] Añadir como argumento de entrada la url.<p>
- [X] Posibiliad que lea fichero html como argumento de entrada<p>
- [X] Añadir como argumento el dominior.<p>
- [X] Añadir marca de tiempo en el fichero de salida.<p>
- [ ] Registro de actividad. Creación de log.<p>



URL test: http://httpbin.org/get <p>
NOTE: test with module torpy =>  pip3 install torpy[requests]<p>
Last update  mié 30 jun 2021 01:14:27 CEST
