from pprint import pprint

listofdevices = ["10.242.1.1", "10.242.1.2", "10.242.1.92", "10.242.1.25", "10.242.1.23"]

dictfacts1 = {"hostname": "SET01", "device": "cisco", "version": "ios"}
dictfacts2 = {"hostname": "SET01", "device": "cisco", "version": "ios"}
dictfacts3 = {"hostname": "SET01", "device": "cisco", "version": "ios"}
dictfacts4 = {"hostname": "SET01", "device": "cisco", "version": "ios"}

listofdictfacts = [dictfacts1,dictfacts2,dictfacts3,dictfacts4]

devices = {}
for device in listofdevices:
    for i in listofdictfacts:
        devices[device] = i
pprint(devices)


print("\nFormatting the information in a nice table")
for device in devices.items():
    print(f"|--{devices.keys()}")
    for value in devices.keys():
        print(value)