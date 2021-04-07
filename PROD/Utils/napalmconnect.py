# This connect script is enabling contact between you and the router
# It will create a dict with hostname and the loopback0
# Then it downloads the running config to the folder/backup/runningcfg.
# This Running config is saved hostname.cfg, afterwards it is used to find strings in 01_find_replace..
# Only when new configuration is ready 02_cfg_replace is used.

import napalm
import copy

from DEV.m02_PlanePython.utils.connect import cisco_site_devices



def getrunningconfig():

    napalm_device = connecttodevice()


    # print(deviceinfo)
    deviceinfo = napalm_device.get_facts()
    interfaces = napalm_device.get_interfaces_ip()

    interface = interfaces["Loopback0"]["ipv4"]

    for loopbackip in interface:
        print(loopbackip)
    deviceinfo["Loopback0"] = loopbackip

    print("\n--------------------------GET Running Config of the device and store it as a separate file")
    # date = str(now.strftime('%d/%m/%Y_%H-%M-%S'))
    with open(f"./backup_runcfg/{deviceinfo['hostname']}.cfg", "w+") as file:
        backup = file.write(napalm_device.get_config()["running"])
        file.close()

    napalm_device.close()
    return (deviceinfo)

def connecttodevice():

    # for loop, with multiple devices in the connect py, this is possible to iterate through.
    try:
        devices = copy.deepcopy(cisco_site_devices)
        for device_type, device in devices.items():
            print(f"\n ----- Connecting to device {device_type}: {device['hostname']} -----")
            driver = napalm.get_network_driver(device_type)
            napalm_device = driver(
                hostname=device["hostname"],
                username=device["username"],
                password=device["password"],
                optional_args={"global_delay_factor": 2}
            )
            napalm_device.open()

            return (napalm_device)

    except Exception as error:
        print(f"################## {error}")
        pass