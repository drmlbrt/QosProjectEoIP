import os
import re
from utils import *

print("="*58)


qos = {'BUISNET': {'remainingbwspeed': 990.0,
             'remainingpercent': 22,
             'string': '#BUISNET#'},
 'BULK': {'remainingbwspeed': 180.0, 'remainingpercent': 4, 'string': '#BULK#'},
 'CALLSIG': {'remainingbwspeed': 90.0,
             'remainingpercent': 2,
             'string': '#CALLSIG#'},
 'HIGHNET': {'remainingbwspeed': 990.0,
             'remainingpercent': 22,
             'string': '#HIGHNET#'},
 'INTERACT': {'remainingbwspeed': 405.0,
              'remainingpercent': 9,
              'string': '#INTERACT#'},
 'NETMGT': {'remainingbwspeed': 225.0,
            'remainingpercent': 5,
            'string': '#NETMGT#'},
 'PUBNET': {'remainingbwspeed': 990.0,
            'remainingpercent': 22,
            'string': '#PUBNET#'},
 'ROUTING': {'remainingbwspeed': 225.0,
             'remainingpercent': 5,
             'string': '#ROUTING#'},
 'SCAVENGER': {'remainingbwspeed': 180.0,
               'remainingpercent': 4,
               'string': '#SCAVENGER#'},
 'TRANSACT': {'remainingbwspeed': 270.0,
              'remainingpercent': 6,
              'string': '#TRANSACT#'},
 'VIDEO': {'remainingbwspeed': 250.0,
           'remainingpercent': 5,
           'string': '#VIDEO#'},
 'VOICE': {'remainingbwspeed': 250.0,
           'remainingpercent': 5,
           'string': '#VOICE#'}}

'''Here we use enumerate to get an index and a value from all lines in text. We do this twice!
First even, find the key of the 'qos' dictionary, then print the first lines of the index. 
In Cisco it is or the first or the second. Probably should add a 'contains not' option to avoid error.
then enumerate the 2 next line, find in the first line the string, if true replace the next index with qos[string]'''


# print("=" * 58)
# fileslist = list(os.listdir("./playbooks/temp/"))
# r = re.compile(r".*PM_QOS_C_[V|NV]")
# newlist = list(filter(r.match, fileslist))
# for index, item in enumerate(newlist):
#     print(f"{index:>5} : {item:>50}")
# choice = int(input(f"What file would you like to change?: "))
# print(newlist[choice])
#
# with open("./playbooks/temp/policy_map_PM_zeroed_values.cfg", "r") as file:
#     listfile = [line.strip() for line in file.readlines()]
#     index = [i for i, item in enumerate(listfile)]
#     for i in index:
#         i = 0
#         new_pm_string = str("policy-map PM_QOS_C_V-70-80-80-80")
#         listfile[i] = new_pm_string
#     print(listfile)
#     with open("./playbooks/temp/policy_map_new_with_zeroed_values.cfg", "w+") as newpmfile:
#         newpmfile.writelines("%s\n" % i for i in listfile)
#         newpmfile.close()
#     with open("./playbooks/temp/policy_map_new_with_zeroed_values.cfg", "r") as newpmfile:
#         print(newpmfile.readlines())
#         newpmfile.close()
# file.close()
#


getdevices = import_from_yaml_single()

for i in getdevices:
    devices = create_devices(i)

    for device in devices.values():

        if not device.connect():
            print(f"----- Connection failed to {device.name}")
            continue
    filename = file_selection()
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




#
# with open("./playbooks/qos/policy_map_PM_QOS_C_V-50-50-0-0.cfg", "r") as file:
#     listfile = [line.strip() for line in file.readlines()]
#     for key, value in qos.items():
#         pattern = str(key)
#         index = [i for i, item in enumerate(listfile) if re.search(pattern, item)]
#         for i in index:
#             i1 = i + 1
#             i2 = i + 2
#             patrn1 = "percent"
#             patrn2 = "bandwidth remaining percent"
#             if patrn1 in listfile[i1]:
#                 lineindex = listfile[i1].strip().split(" ")
#                 # print(f"This is the line splitted in parts {lineindex}")
#                 for index, value in enumerate(lineindex):
#                     if patrn1 == value:
#                         valuepercent = index + 1
#                         lineindex[valuepercent] = str(qos[key]["string"])
#                         listtostring = " "
#                         newstring_forcopy_to_initial_index = listtostring.join(lineindex)
#                         # print(newstring_forcopy_to_initial_index)
#                         listfile[i1] = newstring_forcopy_to_initial_index
#
#             print(f" the new listfile[i1] = {listfile[i1]}")
#             if patrn2 in listfile[i2]:
#
#                 lineindex = listfile[i2].strip().split(" ")
#                 # print(f"This is the line splitted in parts {lineindex}")
#                 for index, value in enumerate(lineindex):
#                     if patrn1 == value:
#                         valuepercent = index + 1
#                         lineindex[valuepercent] = str(qos[key]["string"])
#                         listtostring = " "
#                         newstring_forcopy_to_initial_index = listtostring.join(lineindex)
#                         # print(newstring_forcopy_to_initial_index)
#                         listfile[i2] = newstring_forcopy_to_initial_index
#
#             with open("./playbooks/qos/policy_map_PM_values.cfg", "w+") as change_template_file:
#                 change_template_file.writelines("%s\n" % i for i in listfile)
#                 change_template_file.close()
#     file.close()
