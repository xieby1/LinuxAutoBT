import NetworkManager
import time


def isConnected(state):
    if state == NetworkManager.NM_DEVICE_STATE_IP_CONFIG:
        return True
    if state == NetworkManager.NM_DEVICE_STATE_ACTIVATED:
        return True
    return False


# Compare bdAddr and hwAddr.
# commonly bdAddr looks like
# ['\xb8', "'", '\xeb', '\xc4', 'd', '\xb8'],
# which contain either ASCii chars or Hexadecimal strings,
# should be handled carefully.
def cmpbdhwAddr(bdAddr, hwAddr):
    hwAddrArr = hwAddr.split(':')
    for i in range(6):
        hwAddrDec = int(hwAddrArr[i], 16)
        if len(bdAddr[i]) == 1:
            bdAddrDec = ord(bdAddr[i])
        else:
            bdAddrDec = int(bdAddr[i][2:4], 16)
        if hwAddrDec != bdAddrDec:
            return False
    return True


# hwAddr = "2C:57:31:07:C5:61"  # Tse Hotspot
hwAddr = "30:3A:64:E7:76:00"  # laptop

# firstly, find the connection by hwAddr.
connections = NetworkManager.Settings.ListConnections()
for x in connections:
    if 'bluetooth' in x.GetSettings():
        if cmpbdhwAddr(x.GetSettings()['bluetooth']['bdaddr'], hwAddr):
            connection = x
            break

# secondly, find the device according to hwAddr.
devices = NetworkManager.NetworkManager.GetDevices()
for x in devices:
    if type(x) == NetworkManager.Bluetooth:
        if x.HwAddress == hwAddr:
            device = x
            break

prevState = isConnected(device.State)
if not prevState:
    NetworkManager.NetworkManager.ActivateConnection(connection, device, "/")

maxSleppTime = 64  # in second
sleepTime = 1  # in second
while True:
    curState = isConnected(device.State)
    if prevState and curState:
        time.sleep(sleepTime)
        sleepTime = min(maxSleppTime, sleepTime * 2)
        continue
    elif not prevState and not curState:
        NetworkManager.NetworkManager.ActivateConnection(connection, device, "/")
        time.sleep(sleepTime)
        sleepTime = min(maxSleppTime, sleepTime * 2)
        prevState = curState
        continue
    elif prevState and not curState:
        sleepTime = 1
        prevState = curState
