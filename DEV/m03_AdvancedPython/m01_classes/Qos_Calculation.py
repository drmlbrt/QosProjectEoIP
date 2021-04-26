import decimal
import re
import time
from Device import Device
from copy import deepcopy
from termcolor import colored
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)
from utils import *

class Update_PM_Device():
    '''Here we will define all parts inside the QoS - networks CORP, HIGH, BUISNET, PUBNET'''
    def __init__(self, corpnet=25,
                 highnet=25,
                 buisnet=25,
                 pubnet=25,
                 bandwidth=5000,
                 delay=100,
                 device_name="DEFAULT-SITE-TEST",
                 voice=5,
                 video=5,
                 newpmname="PM_QOS_C_DEFAULT-25-25-25-25",
                 file="Error-with no filename provided"):
        self.newpmname = newpmname
        self.corpnet = int(corpnet)
        self.highnet = int(highnet)
        self.buisnet = int(buisnet)
        self.pubnet = int(pubnet)
        self.bandwidth = int(bandwidth)
        self.delay = int(delay)
        self.device_name = device_name
        self.voice = int(voice)
        self.video = int(video)
        self.new_policy_map_file = str("../playbooks/temp/policy_map_new_"+self.device_name+".cfg")
        self.new_policy_map_file_for_upload = str("../playbooks/temp/policy_map_new_"+self.device_name+"_for_upload.cfg")
        self.line_block = "="*67
        self.ratio_callsig = 10
        self.ratio_interact = 40
        self.ratio_transact = 30
        self.ratio_bulk = 20
        self.file_pm_template = "../playbooks/qos/policy_map_template.cfg"



    def ratio_calc(self):
        '''
        This calculates the ratio of all classes and includes the ratio between different networks. Depending on more
        or less 'bandwidth' provided for PubNet, the ratio shall change. Though, some ratio's are hard coded.
        Be aware of this
        '''

        D = decimal.Decimal


        r_prcnt_scavenger = 4
        r_prcnt_routing = 5
        r_prcnt_netmgt = 5

        r_prcnt_callsig = round(D(((self.corpnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100) * (self.ratio_callsig / 100)))
        r_prcnt_interact = round(D(((self.corpnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100) * (self.ratio_interact / 100)))
        r_prcnt_transact = round(D(((self.corpnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100) * (self.ratio_transact / 100)))
        r_prcent_bulk = round(D(((self.corpnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100) * (self.ratio_bulk / 100)))
        r_prcnt_highnet = round(D((self.highnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100))
        r_prcnt_buisnet = round(D((self.buisnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100))
        r_prcnt_pubnet = round(D((self.pubnet * (100 - r_prcnt_routing - r_prcnt_netmgt - r_prcnt_scavenger)) / 100))

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

        fixedpercent = {"VOICE": self.voice, "VIDEO": self.video}

        qos = {}

        bandwidth = self.bandwidth
        remainingpercent = 100 - sum(fixedpercent.values())

        for key, value in fixedpercent.items():
            form = bandwidth * (value / 100)
            print(f"{key:>12} : {value:>5} % : {form:>7} kbps")
            qos[key] = {"remainingpercent": value, "remainingbwspeed": form, "string": "#" + key + "#"}

        for key, value in remainingclasses.items():
            bandwidthremaining = ((bandwidth * remainingpercent) / 100)
            formula = bandwidthremaining * (value / 100)
            print(f"{key:>12} : {value:>5} % : {round(formula):>7} kbps")
            qos[key] = {"remainingpercent": value, "remainingbwspeed": formula, "string": "#" + key + "#"}


        # new_pm = String_Changer(file=self.filename, qosdict=qos, newpmname=self.newpmname, devicename=self.device_name)
        # new_pm_with_strings = new_pm.make_new_pm()

        print(self.line_block)
        print(f"|---- Replacing the basic template with newly created QoS % values")
        print(f"|---- For a single device: {self.device_name}")

        print(self.line_block)
        print(self.line_block)
        time.sleep(1)

        with open(self.file_pm_template, "r") as file:
            templatestring = file.read()
            file.close()

        for string in qos.values():
            pattern = str(string["string"])
            replacestring = str(string["remainingpercent"])
            templatestring = templatestring.replace(pattern, replacestring, 1)

            with open(self.new_policy_map_file, "w+") as newfile:
                newfile.write(templatestring)
                listoflines = newfile.readlines()
                print(listoflines)
                # listoflines[0] = str("policy-map " + self.newpmname)

                newfile.close()




        time.sleep(1)

        with open(self.new_policy_map_file, "r") as file:
            listfile = [line.strip() for line in file.readlines()]
            pattern = str("bandwidth remaining percent 0")
            patternreplace = "!"
            index = [i for i, item in enumerate(listfile) if re.search(pattern, item)]
            for i in index:
                listfile[i] = patternreplace
            with open(self.new_policy_map_file_for_upload, "w+") as f:
                f.writelines("%s\n" % i for i in listfile)
                f.close()
        file.close()

        time.sleep(1)
        print(f"|----- The new policy map is created : 'PM_QOS_C-{self.corpnet}_{self.highnet}_{self.buisnet}_{self.pubnet}'")

        print(self.line_block)
        print(self.line_block)

        print(f"Ready to send the new file: {self.new_policy_map_file_for_upload}")
        inputquestion = choice()

        inputs = ["yes", "Yes", "Y", "y", "YES"]

        if inputquestion in inputs:
            self.upload_pm()
        else:
            pass

        return

    def upload_pm(self):
        '''
        This where we receive the new policy-map and send it to the device
        '''
        getdevices = import_from_yaml()

        for i in getdevices:
            if self.device_name in i['hostname']:
                devices = create_devices(i)

                for device in devices.values():

                    if not device.connect():
                        print(f"----- Connection failed to {self.device_name}")
                        continue

                with open(self.new_policy_map_file_for_upload, "r") as file:
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

                print(f"\n----- Script has finished his job for {self.device_name}!")
                print(f"\n----- Returning back to menu")
        else:
            print("The Device does not exist in the devices.yaml file ! ")
        return


class String_Changer():
    def __init__(self, file, qosdict, newpmname, devicename):
        self.file = file
        self.qosdict = qosdict
        self.newpmname = newpmname
        self.devicename = devicename
        self.file_location = "../playbooks/temp/"
        self.old_pm_file_location = "../playbooks/temp/policy_map_old_"
        self.line_block = "=" * 67

    def make_new_pm(self):
        print(self.line_block)
        qos = deepcopy(self.qosdict)
        print(f"|---- Replacing all percentage values with #STRING# in the file:  {self.file}")

        with open(self.file, "r") as file:
            listfile = [line.strip() for line in file.readlines()]
            for key, value in qos.items():
                pattern = str(key)
                index = [i for i, item in enumerate(listfile) if re.search(pattern, item)]
                for i in index:
                    i1 = i + 1
                    i2 = i + 2
                    patrn1 = "percent"
                    patrn2 = "bandwidth remaining percent"
                    if patrn1 in listfile[i1]:
                        lineindex = listfile[i1].strip().split(" ")
                        # print(f"This is the line splitted in parts {lineindex}")
                        for index, value in enumerate(lineindex):
                            if patrn1 == value:
                                valuepercent = index + 1
                                lineindex[valuepercent] = str(qos[key]["string"])
                                listtostring = " "
                                newstring_forcopy_to_initial_index = listtostring.join(lineindex)
                                # print(newstring_forcopy_to_initial_index)
                                listfile[i1] = deepcopy(newstring_forcopy_to_initial_index)

                    # print(f" the new listfile[i1] = {listfile[i1]}")
                    if patrn2 in listfile[i2]:
                        lineindex = listfile[i2].strip().split(" ")
                        # print(f"This is the line splitted in parts {lineindex}")
                        for index, value in enumerate(lineindex):
                            if patrn1 == value:
                                valuepercent = index + 1
                                lineindex[valuepercent] = str(qos[key]["string"])
                                listtostring = " "
                                newstring_forcopy_to_initial_index = listtostring.join(lineindex)
                                # print(newstring_forcopy_to_initial_index)
                                listfile[i2] = deepcopy(newstring_forcopy_to_initial_index)
                    time.sleep(1)
                    with open("../playbooks/temp/policy_map_old_" + self.devicename + "_with_zeroed_values.cfg",
                              "w+") as change_template_file:
                        change_template_file.writelines("%s\n" % i for i in listfile)
                        change_template_file.close()
            file.close()

            with open(self.old_pm_file_location + self.devicename + "_with_zeroed_values.cfg", "r") as file:
                listfile = [line.strip() for line in file.readlines()]
                index = [i for i, item in enumerate(listfile)]
                for i in index:
                    i = 0
                    new_pm_string = str("policy-map " + self.newpmname)
                    listfile[i] = new_pm_string
                with open(self.old_pm_file_location + self.devicename + "_with_zeroed_values.cfg", "w+") as newpmfile:
                    newpmfile.writelines("%s\n" % i for i in listfile)
                    thenewfile = newpmfile.name
                    newpmfile.close()

            file.close()
            print(self.line_block)
            print(f"|---- Done replacing all values with the '#' string :  {self.file}")
            print(f"|---- Returning to next step")

        return thenewfile