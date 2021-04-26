import yaml
import json
from pprint import pprint
import os.path
from NapalmDevice import NapalmDevice
from termcolor import colored
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)


def import_from_yaml():
    with open("../playbooks/devices.yaml", "r") as file:
        yamldict = yaml.full_load(file)
        for devices in yamldict.values():
            return devices


def import_from_yaml_single():
    with open("../playbooks/devices_single.yaml", "r") as file:
        yamldict = yaml.full_load(file)
        for devices in yamldict.values():
            return devices


def create_devices(getdevices):
    try:
        created_devices = dict()
        # In Yaml we probably have to adapt the device connection type -> e.g. Wifi Aruba AP's?
        # i shall do this with if device_type == ios then NAPALM device ...

        created_devices["nxos-napalm"] = NapalmDevice(
            name=getdevices["name"],
            hostname=getdevices["hostname"],
            device_type=getdevices["device_type"]
        )
        # unnecessary line, but to show the working of classes Device
        created_devices["nxos-napalm"].set_credentials(username=getdevices["username"], password=getdevices["password"])

        return created_devices

    except Exception as error:
        print(f"################## {error}")
        pass


def getrunningconfig():

    getdevices = import_from_yaml_single()

    for i in getdevices:
        devices = create_devices(i)

        for device in devices.values():

            if not device.connect():
                print(f"----- Connection failed to {device.name}")
                continue

        print("\n----- Get Running Config of the device and store it as a separate file")

        with open(f"../backup_runcfg/{i['name']}.cfg", "w+") as file:
            file.write(device.get_running())
            file.close()


        print("\n----- Running Config store in /backup_runcfg")
        device.disconnect()
        return i['hostname']


def compliance_check():
    compl_os_check = ["15.7(3)M6", "17.3.2"]

    getdevices = import_from_yaml()

    for i in getdevices:
        devices = create_devices(i)

        for _, device in devices.items():

            if not device.connect():
                print(f"----- Connection failed to {device.name}")
                continue

        facts = device.get_facts()
        print(f"----- Facts for device: {device.name}, are checked against compliance.")

        with open("../playbooks/compliance_config.txt", "w+") as file:
            jsonstring = json.dumps(facts, sort_keys=True, indent=4)
            file.write(jsonstring)
            file.close()

        with open("../playbooks/compliance_config.txt", "r") as file:
            stringfile = json.load(file)
            print("="*56)
            print(stringfile["hostname"])

        with open("../playbooks/compliance_check.txt", "w+") as ccfile:
            if not stringfile["hostname"]:
                ccfile.write(f"\n|-- [{stringfile['hostname']:>15}]: Device did not respond to get facts\n")
            else:
                print(f"\n|-- [{stringfile['hostname']:>12}]")
                ccfile.write(f"\n|-- [{stringfile['hostname']:>12}]")
                print(f"|----{stringfile['hostname']:>15} : {stringfile['model']:>20} : {stringfile['vendor']:<20}")
                ccfile.write(f"\n|----{stringfile['hostname']:>15} : {stringfile['model']:>20} : {stringfile['vendor']:<20}")
                print(f"|--------{stringfile['os_version']:>20}")
                ccfile.write(f"\n|--------{stringfile['os_version']:>20}")

                os_version_device = [item.strip() for item in stringfile["os_version"].split(",")]
                os_version = [item.strip() for item in os_version_device[1].split(" ")]

                if any(i in os_version[1] for i in compl_os_check):
                    print(f"|--Version {os_version[1]} OK")
                    ccfile.write(f"\n|--{stringfile['hostname']:<15} : Version {os_version[1]:<10} : OK\n")
                else:
                    print(f"The compliance version {os_version[1]} '-|FAILS|-'")
                    ccfile.write(f"\n|--{stringfile['hostname']:<15} : Version {os_version[1]:<10} : NOT OK\n")
        ccfile.close()
        file.close()
        device.disconnect()


def findstrings(devicename):
    linenum = 0
    dict_of_strings = {"policy_maps" : ["policy-map PM_QOS_"],
                       "class_maps" : ["class-map match-any CM_QOS_",
                       "class-map match-all CM_QOS_"],
                       "acl" :["ip access-list extended ACL_QOS",
                       "ip access-list extended ACL_IP"]}

    print(f"\n----- Looping through strings to find for {devicename}")
    with open(f"../backup_runcfg/{devicename}.cfg","rt") as myfile:
        for line in myfile:
            linenum += 1
            if line.find("QOS") != -1:
                for k, v in dict_of_strings.items():
                    with open("../playbooks/qos/" + k + "_detected.cfg", "a+") as file:
                        for item in v:
                            if item in line:
                                file.write("no " + line)
                    file.close()
    myfile.close()
    return

def get_device_name_from_yaml():
    with open("../playbooks/devices.yaml", "r") as file:
        yamldict = yaml.full_load(file)
        devicename = yamldict['devices'][0]['name']
    return devicename

def choice():
    inputs = ["yes", "Yes", "Y", "y", "YES"]
    inputno = ["no", "No", "N", "n", "NO"]
    txt = "Respond with yes or no?: "
    selection = str(input(Fore.BLACK + Back.YELLOW + txt))
    while True:
        if selection in inputs:
            print(f"You have selected {selection}")
            return selection
        elif selection in inputno:
            print(f"You have selected {selection}")
            return selection
        else:
            print(f"You have entered an invalid selection try: {inputs}")
            break


