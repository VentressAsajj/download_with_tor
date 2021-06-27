# Descarga de url usando privoxy con tor
Bueno sinceramente aún no tengo claro si lo hago con privoxy o solo con tor.<p>
## Instalación y configuración de paquetes
URL test: http://httpbin.org/get<p>

###Installing TOR and privoxy<p>
    apt-get install tor tor-geoipdb privoxy<p>
<p>
###Configuring TOR<p>
        tor --hash-password passhere<p>
    copy the generated hash and add the below lines in configuration file /etc/tor/torrc<p>
        ControlPort 9051<p>
        HashedControlPassword generatedhash<p>
<p>
###Configuring privoxy: add the below lines in configuration file /etc/privoxy/config<p>
        forward-socks5t   /               127.0.0.1:9050 .<p>
        listen-address  127.0.0.1:8118<p>
    optional<p>
        keep-alive-timeout 600<p>
        default-server-timeout 600<p>
        socket-timeout 600<p>
<p>
restart service tor and privoxy<p>
<p>
###Test<p>
    curl http://ifconfig.me # IP<p>
    torify curl http://ifconfig.me # Tor<p>
    curl -x 127.0.0.1:8118 https://ifconfig.me # privoxy/tor<p>
<p>
NOTE: test with module torpy =>  pip3 install torpy[requests]<p><
