from utils import *
from Qos_Calculation import *
import os
import decimal
import re
import time
import yaml
from copy import deepcopy
from termcolor import colored
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)

def get_device_name_from_yaml():
    with open("../playbooks/devices.yaml", "r") as file:
        yamldict = yaml.full_load(file)
        devicename = yamldict['devices'][0]['name']
    return devicename


def single_device_qos_update_policy_map_percentage():
    print("=" * 67)
    fileslist = list(os.listdir("../playbooks/temp/"))
    r = re.compile(r".*PM_QOS_C_[V|NV]")
    newlist = list(filter(r.match, fileslist))
    for index, item in enumerate(newlist):
        print(f"{index:>5} : {item:<50}")
    txt = "What file would you like to change?: "
    choice = int(input(Fore.BLACK + Back.YELLOW + txt))

    filename = newlist[choice]

    print(f"You have : {newlist[choice]}")

    time.sleep(1)

    class_change_parameter_percentage_pm_values(filename)

    return

def file_selection(devicename):
    print("=" * 67)
    fileslist = list(os.listdir("../playbooks/temp/"))
    expression = str(".*"+devicename)
    r = re.compile(expression)
    newlist = list(filter(r.match, fileslist))
    for index, item in enumerate(newlist):
        print(f"{index:>5} : {item:<50}")
    txt = "What file would you like to select?: "
    choice = int(input(Fore.BLACK + Back.YELLOW + txt))
    filename = newlist[choice]
    print(f"You have : {newlist[choice]}")
    return filename


def single_device_qos_update_template():
    getrunningconfig()
    print("=" * 67)
    print("\n----- Make ready for QOS Template update")
    print("=" * 67)
    with open("../playbooks/devices_single.yaml", "r") as file:
        yamldict = yaml.full_load(file)
        for keys in yamldict.values():
           devicename = (keys[0]["name"])

    findstrings(devicename)

    getdevices = import_from_yaml_single()

    for i in getdevices:
        devices = create_devices(i)

        for device in devices.values():

            if not device.connect():
                print(f"----- Connection failed to {device.name}")
                continue
        # Check if the script has created both detected string file and the running config
        # The order of how removing should follow his
        fnamecontrol = [
            "../playbooks/disconnect_servicepolicy.cfg",
            "../playbooks/qos/policy_maps_detected.cfg",
            "../playbooks/qos/class_maps_detected.cfg",
            "../playbooks/qos/acl_detected.cfg",
            "../playbooks/new_qos_template.txt",
        ]

        for i in fnamecontrol:
            if os.path.exists(i):
                print("Files exist: " + i)
            else:
                print("!-!-!-!-!-!-----Script Can't continue, problem with playbooks: " + i)


        for i in fnamecontrol:
            with open((i), "r") as file:
                playbookqostemplate = file.read()
                device.load_config(playbookqostemplate)
                print(f"\n----- Merging the configuration")
                print(f"\n----- Make ready for pushing config from: {i}")
                print(device.compare_config())
                happy = input('Are You happy with this: [yes]') or "yes"
                if happy == 'yes':
                    device.commit_config()
                    print(f"\n---- Pushing Config")
                else:
                    device.discard_config()
                    print(f"\n---- Discarding Config")
        print("=" * 67)
        print(f"\n----- Script has finished his job for {device.name}!")
        print("=" * 67)
        device.disconnect()
        return


def single_device_qos_download_policy_map():
    print("=" * 67)
    print("----- Make ready for QOS - PolicyMap discovery")
    print("=" * 67)
    getdevices = import_from_yaml_single()

    for i in getdevices:
        devices = create_devices(i)

        for device in devices.values():

            if not device.connect():
                print(f"----- Connection failed to {device.name}")
                ipaddressdevice = str(device.name)
                continue
        commands = ["sh ip interface brief | i Tunnel10|Tunnel11|Tunnel12"]
        results = device.clicmd(commands)
        interfaces = []
        for value in results.values():
            result = value.splitlines()
            for index, line in enumerate(result):
                tunnelup = list(filter(None, [line.strip() for line in line.split(" ")]))
                clean = [tunnelup[0], tunnelup[-1]]

                interfaces.append({'interface': clean[0], 'status': clean[1]})

        pprint(interfaces)

        inputs = ["yes", "Yes", "Y", "y"]
        for interface in interfaces:
            if interface["status"] == 'up':
                    inputstrings = [inp.strip() for inp in inputs]
                    choice = input(Fore.BLACK + Back.YELLOW + f"{interface['interface']}  is 'UP' => proceed with template update : ") or inputstrings
                    if choice not in inputstrings:
                        print(f"Invalid choice: {choice}")
                        print(f"---- Returning to menu")
                    else:
                        print(f"---- Getting the policy-map for {interface['interface']}")
                        cmd = ["show policy-map interface " + interface['interface'] + " | i Service-policy : "]
                        policy_map = device.clicmd(cmd)
                        for value in policy_map.values():
                            splittinglist = re.split(r"[ ,\s]\s*", value)
                            r = re.compile("PM_QOS_C_[V|NV]")
                            clean = list(filter(r.match, splittinglist))
                            with open(f"../playbooks/temp/policy_map_old_{device.name}_" + clean[0] +".cfg", "w+") as file:
                                pm = ["show run | s policy-map " + clean[0]]
                                pm_result = device.clicmd(pm)

                                for value in pm_result.values():
                                    file.write(value)
                            file.close()
    return


def send_a_new_pm():

    devicename = input("What is the site IP-LoopBack0: ")

    corpnet = input("What is the value percent for Corpnet: ")
    highnet = input("What is the value percent for Highnet: ")
    buisnet = input("What is the value percent for Buisnet: ")
    pubnet = input("What is the value percent for Pubnet: ")

    print(f"You have entered: {corpnet}-{highnet}-{buisnet}-{pubnet}")
    newpmname = str(f"PM_QOS_C_V-{corpnet}-{highnet}-{buisnet}-{pubnet}")

    txt = colored("Default values for voice, video is 5 %, do you like to change?", "yellow")
    print(txt)

    selection = choice()
    inputs = ["yes", "Yes", "Y", "y", "YES"]

    if selection in inputs:
        print(f"----- Changing the values for Voice & Video")
        voice = input("What is the value percent for Voice: ")
        video = input("What is the value percent for Video: ")
    else:
        print(f"----- Keeping default values for Voice & Video")
        voice = 5
        video = 5

    bandwidth = input("What is the used Bandwidth? : ")
    delay = input("What is the delay for de carrier? : ")


    Style.RESET_ALL

    qos_pm = Update_PM_Device(corpnet, highnet,
                              buisnet,
                              pubnet,
                              bandwidth,
                              delay,
                              devicename,
                              voice,
                              video,
                              newpmname,
                              )
    qos_pm.ratio_calc()

    return