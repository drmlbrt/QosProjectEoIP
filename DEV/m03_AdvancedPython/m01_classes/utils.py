import yaml
import json
from pprint import pprint
from NapalmDevice import NapalmDevice
from NcclientDevice import NcclientDevice


def import_from_yaml():
    with open("../playbooks/devices.yaml", "r") as file:
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
            pprint(stringfile)
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

