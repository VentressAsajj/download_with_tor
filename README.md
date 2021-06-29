# Descarga de url usando privoxy con tor
Bueno sinceramente aún no tengo claro si lo hago con privoxy o solo con tor.<p>
La idea surge a la hora de monitorizar la url donde aparecen las ips que han descargado el malware, el C2.<p>
En principio la descarga la hacía con un simple curl y proxychains, me descargaba el html, lo limpiaba, quedándome solo las ips para luego subirlas
a elasticsearch. Como soy vaga, quiero monitorizar este proceso, descargando la página en formato json. Dejándolo limpio para que pueda cargarlo
con logstash, intentando no perder la fecha del evento y otros datos que son muy interesantes.<p>
Además si cargo los eventos en elastic, y realizando la consulta para obtener el ASN de las IPs, podré generar alertas para instituciones
que son "delicadas".
La generación de ficheros se hace con un cron cada 5'.    

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
- [X] Añadir como argumento el dominio,<p>
- [ ] Registro de actividad. Creación de log.<p>

Decido hacer la ingesta a logstash en vez de usar el modulo de logstash de python. Quizá
lo mire.

Ya he realizado la ingesta en elasticsearch. Al ser un proceso automatizado que se ejecutaba cada 5',
las IPs se repetían y eran eventos duplicados en elasticsearch. Para subsanarlo, he creado un fingerprint
del campo source_ip y vincularlo con el id del documento, de esta manera con cargará los eventos con la misma
IP. No nos interesa puesto que esta IP ya se ha descargado el malware.


URL test: http://httpbin.org/get <p>
NOTE: test with module torpy =>  pip3 install torpy[requests]<p>
Last update: 2021-06-27 17:20:23 Sunday
