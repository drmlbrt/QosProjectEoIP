import napalm
import json
import copy

from connect import cisco_site_devices
# perform a deep copy of my connect.py without messing up the original
devices = copy.deepcopy(cisco_site_devices)
# for loop, with multiple devices in the connect py, this is possible to iterate through.

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
    print("\n ----- These are the NAPALM GETTERS ----")
    print("\n ----- GET FACTS of the device -----")
    print(json.dumps(napalm_device.get_facts(), sort_keys=True, indent=4))

    print("\n ----- GET BGP Neighbors of the device -----")
    print(json.dumps(napalm_device.get_bgp_neighbors(), sort_keys=True, indent=4))

    print("\n ----- GET intefaces IP information  of the device -----")
    print(json.dumps(napalm_device.get_interfaces_ip(), sort_keys=True, indent=4))

    print("\n ----- GET intefaces IP counters information  of the device -----")
    print(json.dumps(napalm_device.get_interfaces_counters(), sort_keys=True, indent=4))

    print("\n ----- GET Running Config of the device -----")
    print(napalm_device.get_config()["running"])

    napalm_device.close()