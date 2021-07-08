from scapy.all import *
from Deauth import change_ch_interface
from classes import StoppableThread, AccessPoint


class defence:
    def __init__(self, AP, interface):
        self.AP = AP
        self.interface = interface
        self.count = 0

    def callback(self, packet):
        if packet.haslayer(Dot11Beacon):
            if self.AP.ssid == packet[Dot11Elt].info.decode() and self.AP.bssid != packet[Dot11].addr2:
                print("sus activity on your router")
        if packet.haslayer(Dot11Deauth):
            self.count = self.count + 1
            if self.count > 40:
                print("sus activity in the air")

    def startSniff(self):
        wifiScan = AsyncSniffer(prn=self.callback, iface=self.interface)
        wifiScan.start()
        channel_changer = StoppableThread(target=self.change_channel)
        channel_changer.daemon = True
        channel_changer.start()

    def change_channel(self):
        ch = 1
        while True:
            os.system(f"iwconfig {self.interface} channel {ch}")
            ch = ch % 14 + 1
            time.sleep(0.5)
