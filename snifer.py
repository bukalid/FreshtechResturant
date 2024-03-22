import scapy.all as scapy

def sniff_network_traffic():
    sniff_filter = scapy.filter.ip.haslayer(scapy.layers.l2.Ether)
    sniff(prn=print_packet, filter=sniff_filter)

def print_packet(pkt):
    if pkt.haslayer(scapy.layers.l2.Ether):
        src_mac = pkt[scapy.layers.l2.Ether].src
        dst_mac = pkt[scapy.layers.l2.Ether].dst
        src_ip = pkt[scapy.layers.l3.IP].src
        dst_ip = pkt[scapy.layers.l3.IP].dst
        print(f"IP Address: {src_ip} | Port: {pkt[scapy.layers.l4.TCP].dport}")

if __name__ == "__main__":
    sniff_network_traffic()