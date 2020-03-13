import argparse
from scapy.layers.inet import TCP, IP, ICMP
from scapy.all import *


def scan():
    open = []
    closed = []
    for port in dst_port:
        rev = sr1(IP(dst=dst_ip) / TCP(sport=src_port, dport=port, flags="F"), timeout=5)
        if not rev:
            open.append(str(port) + "    Probable Open")
        elif rev.haslayer(TCP):
            if rev.getlayer(TCP).flags == "RA":
                closed.append(str(port) + "    Closed")
    print(dst_ip)
    for o in open:
        print(o)
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
    scan()