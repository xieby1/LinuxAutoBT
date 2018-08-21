# LinuxAutoBT: A piece of code can turn on your bluetooth automatically.

## Usage
####0. Dependency:  
- **python-networkmanager** [A set of python wrapped networkmanager api]
```
$ pip install python-networkmanager
```
- **bluetooth.h**  
```
$ sudo apt-get install libbluetooth-dev
```
- **pybluez** [A python wrapped bluez api]
```
$ pip install pybluez
```
####1. Substitude the hwAddr in priortyList with your Bluetooth host hardware address
You can use Bluetoothctl to obtain these two information on your host device like:  
```
$ bluetoothctl
[NEW] ... // here would show your network name
[bluetooth]# show
... // here would show your host hardware address
[bluetooth]# quit
```
####2. Append a commond to /etc/rc.local, then LinuxAutoBT would be excute once startup.  
Example: (You can use whatever text editor with privileged authority)  
```
$ sudo gedit /etc/rc.local
python /THE_FOLDER_OF_LINUXAUTOBT/main.py & # '&' cannot be omitted 
```
####3. Reboot you device and test it

## TODO-LIST
- Add daemon mode
- Add CLI (Command Line Interface)

## Tools and Reference you may need to run and understand LinuxAutoBT:
### NetworkManager - A pre-installed software in most linux os;
Type man NetworkManager into terminal you could get more information
### NetworkManager API (Application Programming Interface)
Here is their [online reference](https://developer.gnome.org/NetworkManager/1.2/spec.html)
### python-networkmanager
A python version of NetworkManager, 
its [Github Page](https://github.com/seveas/python-networkmanager)
### pybluez
A python version of bluez, by which you can access system bluetooth resources, 
its [Github Page](https://github.com/pybluez/pybluez)
### Some Articles about D-Bus
Though I read these articles roughly, and they has less related to the codes, it is good for further study.
[D-Bus Tutorial](https://dbus.freedesktop.org/doc/dbus-tutorial.html)
[dbus-python tutorial](https://dbus.freedesktop.org/doc/dbus-python/tutorial.html)
