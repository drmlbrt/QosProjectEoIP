from tabulate import tabulate
from update_qos_template import *
from termcolor import colored

def menu():
    while True:
        print("=" * 67)
        menudict={
                "01": "All Device Compliance Check.",
                "02": "Replace the complete QOS configuration with new template.",
                "03": "Send and create a new PM for a device.",
                "04": "***",
                "05": "***",
                "06": "***",
                "07": "***",
                "08": "***",
                "09": "Exit the program",
            }
        headers = ["Number", "Called Method"]
        data = sorted([(k, v) for k, v in menudict.items()])
        print(tabulate(data, headers=headers))
        print("=" * 67)
        choice = input("What do you like to do?: ") or '01'

        print("=" * 67)
        if choice == "01":
            print(f"You have selected Process {choice} : {menudict[choice]}")
            compliance_check()
        elif choice == "02":
            print(f"You have selected Process {choice} : {menudict[choice]}")
            single_device_qos_update_template()
        elif choice == "03":
            print(f"You have selected Process {choice} : {menudict[choice]}")
            send_a_new_pm()
        elif choice == "04":
            print(f"You have selected Process {choice} : {menudict[choice]}")
            text = colored(f"Good choice but {choice} does not yet exist", "green")
            print(text)
        elif choice == "05":
            print(f"You have selected Process {choice} : {menudict[choice]}")
            text = colored(f"Good choice but {choice} does not yet exist", "green")
            print(text)
        elif choice == "06":
            print(f"You have selected Process {choice} : {menudict[choice]}")
            text = colored(f"Good choice but {choice} does not yet exist", "green")
            print(text)
        elif choice == "07":
            print(f"You have selected Process {choice} : {menudict[choice]}")
            text = colored(f"Good choice but {choice} does not yet exist", "green")
            print(text)
        elif choice == "08":
            print(f"You have selected Process {choice} : {menudict[choice]}")
            text = colored(f"Good choice but {choice} does not yet exist", "green")
            print(text)
        elif choice == "09":
            print(f"You have selected Process {choice} : {menudict[choice]}")
            text = colored("--- Thank you and please come again ---", "yellow")
            print(text)
            exit()
        else:
            text = colored(f"invalid option, check you input. It needs '0{choice}'", "red")
            print(text)
