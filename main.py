import NetworkManager

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

if device.State != NetworkManager.NM_DEVICE_STATE_ACTIVATED:
    NetworkManager.NetworkManager.ActivateConnection(connection, device, "/")
