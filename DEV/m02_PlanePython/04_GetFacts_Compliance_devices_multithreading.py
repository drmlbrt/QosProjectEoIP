from napalm import get_network_driver
import json


def connecting(host):
    try:
        driver = get_network_driver("ios")
        # Error with IOS 15 - solved with optional arguments src: GitHub support pages
        device = driver(
            hostname=host,
            username="hannibal",
            password="hannibal",
            optional_args={"global_delay_factor": 2},
        )
        device.open()
        facts = device.get_facts()
        print(f"Getting the facts of Host: {host}")
        return (facts)

    except Exception as error:
        print(f"################## {error}")
        pass

listofdevices = [ "10.242.1.92"]
# listofdevices = [ "10.242.1.2",
#                   "10.242.1.1",
#                   "10.242.1.90",
#                   "10.242.1.84",
#                   "10.242.1.85",
#                   "10.242.1.77",
#                   "10.242.1.81",
#                   "10.242.1.23",
#                   "10.242.1.22",
#                   "10.242.1.25"]
#
#
devices = {}
for device in listofdevices:
    facts = connecting(device)
    devices[device] = facts
with open("../m03_AdvancedPython/compliance.config.txt", "w+") as file:
    jsonstring = json.dumps(devices, sort_keys=True, indent=4)
    file.write(jsonstring)
    file.close()

compl_os_check = ["15.7(3)M6", "17.3.2"]

with open("../m03_AdvancedPython/compliance.config.txt", "r") as file:
    stringfile =json.load(file)
    with open("../m03_AdvancedPython/compliance_check.txt", "w+") as ccfile:
        for key, value in stringfile.items():
            if not value:
                ccfile.write(f"\n|-- [{key:>12}]: Device did not respond to get facts\n")
            else:
                print(f"\n|-- [{key:>12}]")
                ccfile.write(f"\n|-- [{key:>12}]")
                print(f"|----{value['hostname']:>15} : {value['model']:>20} : {value['vendor']:<20}")
                ccfile.write(f"\n|----{value['hostname']:>15} : {value['model']:>20} : {value['vendor']:<20}")
                print(f"|--------{value['os_version']:>20}")
                ccfile.write(f"\n|--------{value['os_version']:>20}")

                os_version_device = [item.strip() for item in value['os_version'].split(",")]
                os_version= [item.strip()for item in os_version_device[1].split(" ")]

                if any( i in  os_version[1] for i in compl_os_check):
                    print(f"|--Version {os_version[1]} OK")
                    ccfile.write(f"\n|--{value['hostname']:<15} : Version {os_version[1]:<10} : OK\n")
                else:
                    print(f"Version {os_version[1]} not so OK")
                    ccfile.write(f"\n|--{value['hostname']:<15} : Version {os_version[1]:<10} : NOT OK\n")
    ccfile.close()
file.close()