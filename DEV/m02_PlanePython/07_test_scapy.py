import scapy.all as scapy
from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, ICMP, TCP

# Ping a range of MTU size from you to destination
# first define destination
# then define the range from MTU to MTU
# print the result when ICMP reply is TRUE
# ICMp ping with 'EF' Tag

# Difference made between a TCP ping and UDP ping

print("\n|---- Provide an MTU range size")
# from
mtu_from = 'inputfrom'
mtu_to ='toinput'
# to dst
dst = '8.8.8.8'
# provide destination

ans, unans = scapy.sr(IP(dst=dst)/ICMP())
print(ans.summary())

#discovering hosts via ARP pring

ans, unans = scapy.arping("192.168.1.0/24")
ans.summary()
for res in ans.res:
    print(f"---> IP address discovered: {res[0].payload.pdst}")

