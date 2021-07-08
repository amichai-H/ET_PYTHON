import os
from string import Template
from classes import AccessPoint


def craeteNewAP(interface1, interface2, AP):
    """
    prepare the environment setup for creating the fake access point
    :param AP:
    :param interface2:
    :param interface1:
    """
    os.system('rm -rf build/')
    os.system('cp -r Templates build')
    with open('build/hostapd.conf', 'r+') as f:
        template = Template(f.read())
        f.seek(0)
        f.write(template.substitute(INTERFACE=interface2, NETWORK=AP.ssid))
        f.truncate()
    with open('build/dnsmasq.conf', 'r+') as f:
        template = Template(f.read())
        f.seek(0)
        f.write(template.substitute(INTERFACE=interface2))
        f.truncate()
    with open('build/prepareAP.sh', 'r+') as f:
        template = Template(f.read())
        f.seek(0)
        f.write(template.substitute(INTERFACE=interface2))
        f.truncate()
    with open('build/cleanup.sh', 'r+') as f:
        template = Template(f.read())
        f.seek(0)
        f.write(template.substitute(SNIFFER=interface1, AP=interface2))
        f.truncate()
    os.system('sudo sh build/prepareAP.sh')
