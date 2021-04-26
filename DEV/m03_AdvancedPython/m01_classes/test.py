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


def get_device_name_from_yaml():
    with open("../playbooks/devices.yaml", "r") as file:
        yamldict = yaml.full_load(file)
        devicename = yamldict['devices'][0]['name']
    return devicename

devicename = get_device_name_from_yaml()


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
#First we create an instance of the d object
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

exit()