from scapy.all import sniff, IP, TCP

def packet_callback(packet):
    if packet[TCP].payload:
        mypacket = str(packet[TCP].payload)
        if "user" or "pass" in mypacket.lower():
            print(f"Destination: {mypacket[IP].dst}")
            print(f"{mypacket}")

def main():
    sniff(filter="tcp port 110 or tcp port 25", prn=packet_callback, store=0 )

if __name__ == "__main__":
    main()