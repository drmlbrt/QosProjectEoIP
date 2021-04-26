"""
Import the devices from the devices Yaml file,
Request which one you like to connect to,
Request what you would like to do,
'warning' depending on the amount of devices some 'get's' can take a long time.

devices have common facts such as :
- 'HOST name' Ip address -> for Napalm this is the IP address where we connect to: we do not use DNS
- device type: IOS -> needed for the napalm
- a name: SITE_XXX

First we define the 'Base' Device class, that calls the subordinate Class to connect to the device and to have sub-Classes
that are able to get:
- Connect
- Disconnect
- Get Facts
- Get QoS information (Class)
- Get Running Config
- Replace Parts: start with QoS and gradually build up...

This yaml file should be created after discovery and you can always add fixed 'devices' by following the syntax

"""
from menu import menu

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("="*56)
        print("\nExiting the program")
        print("="*56)