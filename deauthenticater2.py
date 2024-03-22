import scapy.all as scapy

def deauthenticate_clients(ap_mac, deauth_reason=None):
    # Define the deauthentication frame
    deauth = scapy.WLANDeauth(addr=ap_mac)
    if deauth_reason:
        deauth.reason = deauth_reason

    # Send the deauthentication frame
    sendp(deauth, verbose=0)

def detect_rogue_aps():
    rogue_aps = set()
    for i in range(10):
        # Try to find rogue access points in monitor mode for 10 seconds
        r = scapy.sniff(list_rate=True)

        # For each rogue access point found, get its BSSID and SSID
        for pkt in r:
            if pkt.type == "WLANBeacon" and (pkt.addr2 not in ap_addresses):
                print(f"Detected rogue AP with SSID '{pkt.info}' and BSSID '{pkt.addr2}'")
                ap_addresses.add(pkt.addr2)
                rogue_aps.add((pkt.info, pkt.addr2))

    return rogue_aps

ap_addresses = set()  # Set of known APs' addresses
ap_macs = []  # List of APs' BSSIDs
known_ap_ssids = set()  # Set of known APs' SSIDs

while True:
    try:
        # Try to deauthenticate all clients from a known AP
        rogue_aps = detect_rogue_aps()
        for (ssid, bssid) in rogue_aps:
            deauthenticate_clients(bssid)

        print("Scan complete. Looking for known APs...")

        # Get all BSSIDs in the current scanning radius
        active_ap_bssids = set()
        r = scapy.sniff(prn=lambda x: x.type == "WLANBeacon" and x.info not in known_ap_ssids, verbose=0)

        # For each Beacon packet found, save its SSID and BSSID
        for pkt in r:
            if pkt.info not in known_ap_ssids:
                known_ap_ssids.add(pkt.info)
                active_ap_bssids.add(pkt.addr2)
                ap_ssids.append(pkt.info)
                ap_macs.append(pkt.addr2)

        print(f"Detected {len(ap_ssids)} access points: {ap_ssids}")
        print(f"Associated clients (BSSID): {active_ap_bssids}")
    except Exception as e:
        print(e)
        pass