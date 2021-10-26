# Network Utilities

## config

netsh interface ipv4 show config

netsh interface ipv4 set address    name="YOUR INTERFACE NAME" static IP_ADDRESS SUBNET_MASK GATEWAY
netsh interface ipv4 set address    name="Wi-Fi" static 192.168.3.8 255.255.255.0 192.168.3.1
netsh interface ipv4 set address    name=”YOUR INTERFACE NAME” source=dhcp

netsh interface ipv4 set dns        name="YOUR INTERFACE NAME" static DNS_SERVER
netsh interface ipv4 set dns        name="Wi-Fi" static 8.8.8.8
netsh interface ipv4 set dns        name="YOUR INTERFACE NAME" static DNS_SERVER index=2
netsh interface ipv4 set dns        name="Wi-Fi" static 8.8.4.4 index=2
netsh interface ipv4 set dnsservers name"YOUR INTERFACE NAME" source=dhcp

## ping

## ipconfig/ifconfig

	> ipconfig /all

## traceroute/tracert/tracepath
## nslookup
## whois
## netstat
## finger/nmap

