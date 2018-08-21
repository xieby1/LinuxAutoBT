import NetworkManager
import time
import bluetooth


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
################### END OF FUNC DEF #########################

# Add your host device hardware address here
# TIP: the entry nearer the list top has higher priority
priorityList = [
                "30:3A:64:E7:76:00",    # laptop
                "2C:57:31:07:C5:61"     # Tse Hotspot
                ]


prevState = False
#logFile = open("state logs", 'a')
#logFile.write(str(temp_ds) + " " + NetworkManager.const('device_state', temp_ds) + '\n')
#logFile.close()
hwAddr = ""
maxSleppTime = 64  # in second
sleepTime = 1  # in second
while True:
    if len(hwAddr) == 0:
        curState = False
    else:
        curState = isConnected(device.State)
    if prevState and curState:
        sleepTime = min(maxSleppTime, sleepTime * 2)
    elif not prevState and not curState:
        available_services = bluetooth.find_service(uuid=bluetooth.NAP_CLASS)
        hwAddr = ""
        for list_device in priorityList:
            for available_service in available_services:
                if available_service["host"] == list_device:
                    hwAddr = list_device
                    break
            if len(hwAddr) > 0:
                break
        if len(hwAddr)>0:
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

            NetworkManager.NetworkManager.ActivateConnection(connection, device, "/")

        sleepTime = min(maxSleppTime, sleepTime * 2)
    else:  # not prevState and curState or prevState and not curState::
        sleepTime = 1

    time.sleep(sleepTime)
    prevState = curState
 #   logFile = open("state logs", 'a')
  #  logFile.write(str(temp_ds) + " " + NetworkManager.const('device_state', temp_ds) + '\n')
   # logFile.close()
