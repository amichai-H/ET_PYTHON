import subprocess
import os


def scanForDevice():
    results = subprocess.check_output(["ip", "-br", "link", "show"])
    results = results.decode("ascii")
    device_list = results.split("\n")
    device_filter = []
    x = 0
    while x < len(device_list):
        first = device_list[x].split(" ")
        word = first[0]
        if word != " " and word.startswith("wlx"):
            device_filter.append(word)
        x += 1
    return device_filter


def check_user_input(input1):
    while 1:
        try:
            val = int(input1)
            return val
        except ValueError:
            print("No.. input is not a number. It's a string try again")
            input1 = input()


def chooseInterface(massage):
    print(massage)
    devices = scanForDevice()
    i = 0
    for device in devices:
        if len(device) > 0:
            print(str(i + 1) + ". " + device)
        i = i + 1
    print("Please choose a device from the list above")
    index = check_user_input(input(">"))
    return devices[index - 1]


def startMonitorMode(iface):
    os.system(f"sudo ifconfig {iface} down")
    os.system(f"sudo iwconfig {iface} mode monitor")
    os.system(f"sudo ifconfig {iface} up")


def bar60Sec():
    from time import sleep
    import sys

    for i in range(61):
        sys.stdout.write('\r')
        sys.stdout.write("[%-60s] %d%%" % ('=' * i, (100 / 60) * i))
        sys.stdout.flush()
        sleep(1)
