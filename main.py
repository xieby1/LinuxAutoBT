import NetworkManager
import time

def isConnected (state):
    if state == NetworkManager.NM_DEVICE_STATE_IP_CONFIG:
        return True
    if state == NetworkManager.NM_DEVICE_STATE_ACTIVATED:
        return True
    return False

hwAddr = "2C:57:31:07:C5:61"
name = "TseHotspot Network"
connections = NetworkManager.Settings.ListConnections()
for x in connections:
    if x.GetSettings()['connection']['id'] == name:
        connection = x
        break

devices = NetworkManager.NetworkManager.GetDevices()
for x in devices:
    if type(x) == NetworkManager.Bluetooth:
        if x.HwAddress == hwAddr:
            device = x
            break

prevState = isConnected(device.State)
if not prevState:
    NetworkManager.NetworkManager.ActivateConnection(connection, device, "/")

maxSleppTime = 64 # in second
sleepTime = 1  # in second
while True:
    curState = isConnected(device.State)
    if prevState and curState:
        time.sleep(sleepTime)
        sleepTime = min(maxSleppTime, sleepTime*2)
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
