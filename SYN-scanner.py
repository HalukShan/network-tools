import argparse
from scapy.layers.inet import TCP, IP, ICMP
from scapy.all import *


def scan():
    open = []
    filtered = []
    closed = []
    for port in dst_port:
        rev = sr1(IP(dst=dst_ip) / TCP(sport=src_port, dport=port, flags="S"), timeout=10)
        if not rev:
            filtered.append(str(port) + "    Filtered")
        elif rev.haslayer(TCP):
            if rev.getlayer(TCP).flags == "SA":
                send(IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="RA"))
                open.append(str(port) + "    Open")
            elif rev.getlayer(TCP).flags == "RA":
                closed.append(str(port) + "    Closed")
        # Intercepted !
        elif rev.haslayer(ICMP):
            if int(rev.getlayer(ICMP).type) == 3 and int(rev.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]:
                print("Filtered")
                filtered.append(rev)
    print(dst_ip)
    for o in open:
        print(o)
    for f in filtered:
        print(f)
    for c in closed:
        print(c)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dst_ip", help="Destination ip address", type=str)
    parser.add_argument("dst_port", help="Display a cubic of a given number", nargs='+', type=int)
    args = parser.parse_args()
    dst_ip = args.dst_ip
    dst_port = args.dst_port
    src_port = RandShort()
    print(dst_port)
    scan()
