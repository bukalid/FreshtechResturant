import scapy.all as scapy
import mysql.connector

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
        # Connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="network_traffic"
        )

        # Create table if it doesn't exist
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS packet_data (mac_src VARCHAR(255), mac_dst VARCHAR(255), ip_src VARCHAR(255), ip_dst VARCHAR(255), port VARCHAR(255))")

        # Insert data into MySQL database
        cursor.execute("INSERT INTO packet_data VALUES (%s, %s, %s, %s, %s)", packet_data)
        db.commit()
        cursor.close()
        db.close()

if __name__ == "__main__":
    sniff_network_traffic()