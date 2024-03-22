class ICMP(Structure):
 _fields_ = [
 ("type", c_ubyte),
 ("code", c_ubyte),
 ("checksum", c_ushort),
 ("unused", c_ushort),
 ("next_hop_mtu", c_ushort)
 ]
 def __new__(self, socket_buffer):
 return self.from_buffer_copy(socket_buffer)
 def __init__(self, socket_buffer):
 pass
--snip--
 print "Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_¬
address, ip_header.dst_address)
 # if it's ICMP, we want it
v if ip_header.protocol == "ICMP":
 # calculate where our ICMP packet starts
w offset = ip_header.ihl * 4
44 Chapter 3
 buf = raw_buffer[offset:offset + sizeof(ICMP)]
 # create our ICMP structure
x icmp_header = ICMP(buf)
 print "ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.¬
code)