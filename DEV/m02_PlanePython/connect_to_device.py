from napalm import get_network_driver
import json

def connecttodevice(hostname, username, password):


    driver = get_network_driver("ios")
    device = driver(hostname=hostname,
                    username=username,
                    password=password,
                    )
    device.open()
    # This is a copy paste from an older test file ! So it does not work . Just
    if info == '1':
        information = list()
        getfacts = json.dumps(device.get_facts(), indent=2)
        version = json.loads(getfacts)
        # version_info = (version["os_version"])
        # host_name = (version["hostname"])
        # model_name = (version["model"])
        print(f"{version['hostname']} {version['vendor']} {version['model']} {version['os_version']}")
        version_info_clean = version_info.split(",")
        for part_no, version_info_part in enumerate(version_info_clean):
            information.append(f"Version part {part_no}: {version_info_part.strip()}")

        # information = version_info.split(",")
    elif info == '2':
        information = json.dumps(device.get_interfaces_ip(), indent=4)
    else:
        information = (device.get_config()['running'])

    return information