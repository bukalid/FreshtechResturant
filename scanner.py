import threading
import time
from netaddr import IPNetwork,IPAddress
--snip--
# host to listen on
host = "192.168.0.187"
# subnet to target
subnet = "192.168.0.0/24"
# magic string we'll check ICMP responses for
u magic_message = "PYTHONRULES!"
# this sprays out the UDP datagrams
v def udp_sender(subnet,magic_message):
 time.sleep(5)
 sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 for ip in IPNetwork(subnet):
The Network: Raw Sockets and Sniffing 45
 try:
 sender.sendto(magic_message,("%s" % ip,65212))
 except:
 pass
--snip--
# start sending packets
w t = threading.Thread(target=udp_sender,args=(subnet,magic_message))
t.start()
--snip--
try:
 while True:
 --snip--
 #print "ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.¬
code)
 # now check for the TYPE 3 and CODE
 if icmp_header.code == 3 and icmp_header.type == 3:
 # make sure host is in our target subnet
x if IPAddress(ip_header.src_address) in IPNetwork(subnet):
 # make sure it has our magic message
y if raw_buffer[len(raw_buffer)-len(magic_message):] == ¬
magic_message:
 print "Host Up: %s" % ip_header.src_address