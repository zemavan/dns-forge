#!/usr/bin/env python3
import os

ask_option = input("Port for dns: ")
zone_name = input("name for zone: ")



content_options = f"""
options {{
    directory "/var/cache/bind";

    listen-on port {ask_option} {{ 127.0.0.1; }}; # Escuchar en todas las interfaces IPv4
    listen-on-v6 port {ask_option} {{ ::1; }}; # Escuchar en todas las interfaces IPv6

    recursion yes; # Permitir consultas recursivas
    allow-recursion {{ any; }}; # Permitir recursi  n desde cualquier IP

}};
"""

with open("/etc/bind/named.conf.options", "w") as f:
    f.write(content_options)
    print("Config written successfully")
    f.close()

os.system("cat /etc/bind/named.conf.options")


print("configure next named.conf.options")


content_local = f"""
zone "{zone_name}" {{
  type master;
  file "/etc/bind/zones/db.{zone_name}";
}};
"""

with open("/etc/bind/named.conf.local", "w") as f:
    f.write(content_local)
    f.close()

os.system("cat /etc/bind/named.conf.local")


os.system("mkdir -p /etc/bind/zones")
os.system(f"touch /etc/bind/zones/db.{zone_name}")


config_zone = input('ip for root and ns1: ')
content_zone = f"""
$TTL    604800
@   IN  SOA ns1.{zone_name}. admin.{zone_name}. (
                2024010101 ; Serial
                604800     ; Refresh
                86400      ; Retry
                2419200    ; Expire
                604800 )   ; Negative Cache TTL
 
; Servidores de nombres
@   IN  NS  ns1.{zone_name}.
 
; Registros A
@   IN  A   {config_zone}
ns1 IN  A   {config_zone}
www IN  A   {config_zone}
"""

with open(f"/etc/bind/zones/db.{zone_name}", "w") as f:
    f.write(content_zone)
    f.close()

os.system(f"cat /etc/bind/zones/db.{zone_name}")
os.system("/usr/sbin/named -g -c /etc/bind/named.conf")

