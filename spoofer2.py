import scapy.all as scapy
import mysql.connector

def spoof_mac_address(target_mac, spoof_mac):
    # Define the Ethernet II packet
    eth = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    eth.add_layer(scapy.Ether(src=target_mac))

    # Spoof the MAC address in the Ethernet II packet
    eth.payload = scapy.Raw(b"\x08\x00" + spoof_mac + b"\x00\x00")

    # Send the spoofed packet
    sendp(eth, verbose=0)

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

def main():
    target_mac = "00:11:22:33:44:55"
    spoof_mac = "66:77:88:99:aa:bb"
    spoof_mac_address(target_mac, spoof_mac)

    extract_packet_data(pkt)

if __name__ == "__main__":
    main()