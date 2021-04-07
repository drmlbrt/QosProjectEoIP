from tabulate import tabulate
from utils import *

def menu():

    menudict=\
        {
            "01": "All Device Compliance Check",
            "02": "Single Device Update QoS template",
            "03": "Single Device Update QoS Policy-Map",
            "04": "Single Device Check EIGRP load Balancing",
            "05": "***",
            "06": "***",
            "07": "***",
            "08": "***",
            "09": "***",
        }
    headers = ["Number", "Called Method"]
    data = sorted([(k,v ) for k, v in menudict.items()])
    print(tabulate(data, headers=headers))

    choice = input("What do you like to do?: ") or '01'
    print(f"You have selected Process {choice} : {menudict[choice]}")

    if choice == "01":
        compliance_check()
