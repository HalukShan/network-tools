# G-scanner
This is a rep that I write for learning protocols.
All about scanning tools write in python. These scanners are based 
on the TCP or UDP protocols to scan alive ports on specified host.
**Now it is not complete**.

## SYN Scanner
This scanner is based on the incomplete TCP handshake 
connection. After we sends the SYN message, the 
target will reply to the SYN + ACK message, which means 
that the specified target port is open, but we 
will reply to an RST, which in TCP flags is "R" to close
the TCP connection.
```
sudo python3 SYN-scanner.py dstip dport1 dport2 ...
```

## FIN Scanner
The Fin-scan, If no service is listening on the target port, the target 
system generates an RST message, and we will receive immediately.
 If the service is listening, the operating system silently discards the incoming packets.
 As a result, there is no response indicating that there is 
 a listening service on the port. But sometimes it's the 
 firewall that filters

