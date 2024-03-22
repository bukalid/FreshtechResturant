import scapy.all as scapy
import csv

def sniff_network_traffic():
    sniff_filter = scapy.filter.ip.haslayer(scapy.layers.l2.Ether)
    sniff(prn=extract_packet_data, filter=sniff_filter)

def extract_packet_data(pkt):
    if pkt.haslayer(scapy.layers.l2.Ether):
        src_mac = pkt[scapy.layers.l2.Ether].src
        dst_mac = pkt[scapy.layers.l2.Ether].dst
        src_ip = pkt[scapy.layers.l3.IP].src
        dst_ip = pkt[scapy.layers.l3.IP].dst
        port = pkt[scapy.layers.l4.TCP].dport

        packet_data = [src_mac, dst_mac, src_ip, dst_ip, port]
        print(packet_data)
        with open('packet_data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(packet_data)

if __name__ == "__main__":
    sniff_network_traffic()