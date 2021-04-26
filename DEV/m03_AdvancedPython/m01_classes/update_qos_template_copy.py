from utils import *
import Qos_Calculation
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


def clean_pm_zero_values(devicename):
    with open("../playbooks/temp/policy_map_new_"+ devicename +".cfg", "r") as file:
        listfile = [line.strip() for line in file.readlines()]
        pattern = str("bandwidth remaining percent 0")
        patternreplace = "!"
        index = [i for i, item in enumerate(listfile) if re.search(pattern, item)]
        for i in index:
           listfile[i] = patternreplace
        with open("../playbooks/temp/policy_map_new_"+ devicename +"_for_upload.cfg", "w+") as f:
            f.writelines("%s\n" % i for i in listfile)
            f.close()
    file.close()
    return


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


def single_device_qos_update_policy_map():
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
                            filename = file.name
                            file.close()
    return filename

def class_change_parameter_percentage_pm_values(filename):

    devicename = get_device_name_from_yaml()
    # the Decimal function minimize the rounding issues, but not eliminates

    corpnet = input("What is the value percent for Corpnet: ")
    highnet = input("What is the value percent for Highnet: ")
    buisnet = input("What is the value percent for Buisnet: ")
    pubnet = input("What is the value percent for Pubnet: ")
    print(f"You have entered: {corpnet}-{highnet}-{buisnet}-{pubnet}")
    pmname = str(f"PM_QOS_C-{corpnet}-{highnet}-{buisnet}-{pubnet}")
    txt = colored("Default values for voice, video is 5 %, do you like to change?", "yellow")
    print(txt)
    selection = choice()
    inputs = ["yes", "Yes", "Y", "y", "YES"]
    if selection in inputs:
        print(f"----- Changing the values for Voice & Video")
        voice = input("What is the value percent for Voice: ")
        video = input("What is the value percent for Video: ")
        fixedpercent = {"VOICE": int(voice),
                        "VIDEO": int(video),
                        }
    else:
        print(f"----- Keeping default values for Voice & Video")
        voice = 5
        video = 5
        fixedpercent = {"VOICE": int(voice),
                        "VIDEO": int(video),
                        }

    bandwidth = input("What is the used Bandwidth? : ")
    delay = input("What is the delay for de carrier? : ")


    Style.RESET_ALL

    Qos_Calculation.Qoscalc(corpnet, highnet, buisnet, pubnet, bandwidth, delay, devicename, voice, video)

    return


def change_parameter_percentage_pm_values(filename):
    D = decimal.Decimal
    devicename = get_device_name_from_yaml()
    # the Decimal function minimize the rounding issues, but not eliminates


    corpnet = int(input("What is the value percent for Corpnet: ") or "25")
    highnet = int(input("What is the value percent for Highnet: ") or "25")
    buisnet = int(input("What is the value percent for Buisnet: ") or "25")
    pubnet = int(input("What is the value percent for Pubnet: ") or "25")
    print(f"You have entered: {corpnet}-{highnet}-{buisnet}-{pubnet}")
    pmname = str(f"PM_QOS_C-{corpnet}-{highnet}-{buisnet}-{pubnet}")
    txt = colored("Default values for voice, video is 5 %, do you like to change?", "yellow")
    print(txt)
    selection = choice()
    inputs = ["yes", "Yes", "Y", "y", "YES"]
    if selection in inputs:
        print(f"----- Changing the values for Voice & Video")
        voice = input("What is the value percent for Voice: ")
        video = input("What is the value percent for Video: ")
        fixedpercent = {"VOICE": int(voice),
                        "VIDEO": int(video),
                        }
    else:
        print(f"----- Keeping default values for Voice & Video")
        voice = 5
        video = 5
        fixedpercent = {"VOICE": int(voice),
                        "VIDEO": int(video),
                        }
    Style.RESET_ALL


    # adapting the ratio for interact transact and bulk traffic is to be done manually.

    ratio_callsig = 10
    ratio_interact = 40
    ratio_transact = 30
    ratio_bulk = 20

    print("=" * 67)

    r_prcnt_scavenger = 4
    r_prcnt_routing = 5
    r_prcnt_netmgt = 5
    r_prcnt_callsig = round(
        D(((corpnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100) * (ratio_callsig / 100)))
    r_prcnt_interact = round(
        D(((corpnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100) * (ratio_interact / 100)))
    r_prcnt_transact = round(
        D(((corpnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100) * (ratio_transact / 100)))
    r_prcent_bulk = round(
        D(((corpnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100) * (ratio_bulk / 100)))
    r_prcnt_highnet = round(D((highnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100))
    r_prcnt_buisnet = round(D((buisnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100))
    r_prcnt_pubnet = round(D((pubnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100))

    totalremaininglist = [r_prcnt_scavenger, r_prcnt_routing, r_prcnt_netmgt, r_prcnt_callsig, r_prcnt_interact,
                          r_prcnt_transact, r_prcent_bulk, r_prcnt_highnet, r_prcnt_buisnet, r_prcnt_pubnet]

    totalremaining = sum(totalremaininglist)

    print(f"the totalremaining: {totalremaining}% -> if more then 100 or lower, will be solved automatically")

    remainingclasses = {
        "ROUTING": r_prcnt_routing,
        "NETMGT": r_prcnt_netmgt,
        "CALLSIG": r_prcnt_callsig,
        "INTERACT": r_prcnt_interact,
        "TRANSACT": r_prcnt_transact,
        "BULK": r_prcent_bulk,
        "HIGHNET": r_prcnt_highnet,
        "BUISNET": r_prcnt_buisnet,
        "PUBNET": r_prcnt_pubnet,
        "SCAVENGER": r_prcnt_scavenger}

    qos = {}
    bandwidth = 5000
    remainingpercent = 100 - sum(fixedpercent.values())

    print("=" * 67)

    time.sleep(1)

    for key, value in fixedpercent.items():
        form = bandwidth * (value / 100)
        print(f"{key:>12} : {value:>5} % : {form:>7} kbps")
        qos[key] = {"remainingpercent": value, "remainingbwspeed": form, "string": "#" + key + "#"}

    for key, value in remainingclasses.items():
        bandwidthremaining = ((bandwidth * remainingpercent) / 100)
        formula = bandwidthremaining * (value / 100)
        print(f"{key:>12} : {value:>5} % : {round(formula):>7} kbps")
        qos[key] = {"remainingpercent": value, "remainingbwspeed": formula, "string": "#" + key + "#"}

    new_pm_with_strings = make_new_pm_with_string(file=filename, qosdict=qos, newpmname=pmname)

    print(f"|---- Replacing the template with created QoS % values")
    print(f"|---- For single device")
    print("_" * 67)
    time.sleep(1)

    with open(new_pm_with_strings, "r") as file:
        templatestring = file.read()
        file.close()
    for string in qos.values():
        pattern = str(string["string"])
        replacestring = str(string["remainingpercent"])
        templatestring = templatestring.replace(pattern, replacestring, 1)
    with open("../playbooks/temp/policy_map_new_"+devicename+".cfg", "w+") as newfile:
        newfile.write(templatestring)
        newfile.close()
    print(f"|---- Cleaning the new PM from 'zero' values")
    clean_pm_zero_values(devicename)


    print("=" * 67)
    time.sleep(1)
    print(f"|----- The new policy map is created : 'PM_QOS_C-{corpnet}_{highnet}_{buisnet}_{pubnet}'")
    print(f"|----- Returning to menu for next step")
    time.sleep(1)
    return

# def make_new_pm_with_string(file, qosdict, newpmname):
#     time.sleep(2)
#     qos = deepcopy(qosdict)
#     filename = file
#     devicename = get_device_name_from_yaml()
#     thenewfile = Qos_Calculation.String_Changer(file, qosdict, newpmname, devicename)
#     return thenewfile


def upload_new_pm_for_single_device():
    getdevices = import_from_yaml_single()

    for i in getdevices:
        devices = create_devices(i)

        for device in devices.values():

            if not device.connect():
                print(f"----- Connection failed to {device.name}")
                continue
        filename = file_selection(devicename=device.name)
        with open("../playbooks/temp/" + filename, "r") as file:
            newpmtemplate = file.read()
            device.load_config(newpmtemplate)
            print(f"\n----- Merging the configuration")
            print(f"\n----- Make ready for pushing config")
            print(device.compare_config())

            happy = choice()
            inputs = ["yes", "Yes", "Y", "y", "YES"]
            if happy in inputs:
                device.commit_config()
                print(f"\n----- Pushing Config")
            else:
                device.discard_config()
                print(f"\n----- Discarding Config")
        print("=" * 67)

        print(f"\n----- Script has finished his job for {device.name}!")
        print(f"\n----- Returning back to menu")
    return