import scapy.all as scapy

def spoof_mac_address(target_mac, spoof_mac):
    # Define the Ethernet II packet
    eth = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    eth.add_layer(scapy.Ether(src=target_mac))

    # Spoof the MAC address in the Ethernet II packet
    eth.payload = scapy.Raw(b"\x08\x00" + spoof_mac + b"\x00\x00")

    # Send the spoofed packet
    sendp(eth, verbose=0)

# Example usage:
target_mac = "00:11:22:33:44:55"
spoof_mac = "66:77:88:99:aa:bb"
spoof_mac_address(target_mac, spoof_mac)