This is a rep of network tools that I use to learn protocols and practice 
in Python. 
## arpspoof
ARP Spoofing... Usage
```
sudo python3 arpspoof.py target_ip gateway_ip interface
```
## arppoison-cross-vlan
ARP posion cross vlan, base on the switch with trunk environment, the 
script can cross vlan to broke the other vlan devices network conncetion 
with gateway, but the other devices must locate in the another side 
of the trunk, usage
```
sudo python3 arppoison-cross-vlan.py -g gateway_ip -sv self_vlan -tv (single or range of vlan like 2-100) -i iface
```



## SYN Scanner
This scanner is based on the incomplete TCP handshake 
connection. After we sends the SYN message, the 
target will reply to the SYN + ACK message, which means 
that the specified target port is open, but we'll gonna to
 reply the RST, which in TCP flags is "RA" to close
the TCP connection.
```
sudo python3 SYN-scanner.py dstip dport1 dport2 ...
```

## FIN Scanner
The Fin-scan, If no service is listening on the target port, the target 
system generates an RST message, and we will receive immediately.
 If the service is listening, the operating system silently discards the incoming packets.
 As a result, there is no response indicating that there is 
 a listening service on the port. But sometimes it's filtered
 by firewall
```
sudo python3 FIN-scanner.py dstip dport1 dport2 ...
```

Still on...