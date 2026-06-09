#!/usr/bin/env python3
import os

content_options = """
options {
    directory "/var/cache/bind";

    listen-on port 1053 { 127.0.0.1; }; # Escuchar en todas las interfaces IPv4
    listen-on-v6 port 1053 { ::1; }; # Escuchar en todas las interfaces IPv6

    recursion yes; # Permitir consultas recursivas
    allow-recursion { any; }; # Permitir recursi  n desde cualquier IP

};
"""

with open("/etc/bind/named.conf.options", "w") as f:
    f.write(content_options)
    print("Config written successfully")
    f.close()

os.system("cat /etc/bind/named.conf.options")


print("configure next named.conf.options")


content_local = """
zone "fruit.com" {
  type master;
  file "/etc/bind/zones/db.fruit.com";
};
"""

with open("/etc/bind/named.conf.local", "w") as f:
    f.write(content_local)
    f.close()

os.system("cat /etc/bind/named.conf.local")


os.system("mkdir -p /etc/bind/zones")
os.system("touch /etc/bind/zones/db.fruit.com")

with open("/etc/bind/zones/db.fruit.com", "w") as f:
    f.write("""
$TTL    604800
@   IN  SOA ns1.fruit.com. admin.fruit.com. (
                2024010101 ; Serial
                604800     ; Refresh
                86400      ; Retry
                2419200    ; Expire
                604800 )   ; Negative Cache TTL
 
; Servidores de nombres
@   IN  NS  ns1.fruit.com.
 
; Registros A
@   IN  A   172.17.0.3
ns1 IN  A   172.17.0.3
www IN  A   172.17.0.3
""")
    f.close()

os.system("cat /etc/bind/zones/db.fruit.com")
os.system("/usr/sbin/named -g -c /etc/bind/named.conf")


