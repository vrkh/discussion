import subprocess
from getmac import get_mac_address


def get_pc_info():
    cmd = 'wmic csproduct get uuid'
    hwid = str(subprocess.check_output(cmd, shell=True))
    pos1 = hwid.find("\\n") + 2
    hwid = hwid[pos1:-15]
    mac = get_mac_address()

    return str(hwid), str(mac)
