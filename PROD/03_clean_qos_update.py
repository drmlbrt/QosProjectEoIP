from DEV.m02_PlanePython.utils.napalmconnect import getrunningconfig
from DEV.m02_PlanePython.utils.napalmconnect import connecttodevice
from DEV.m02_PlanePython.utils.findstrings import findstrings
from copy import deepcopy
import os.path

if __name__ == '__main__':
    print("\n--------------------------Connecting to devices configured in the connect! Verify this before")
    device = getrunningconfig()
    print("\n--------------------------Finding the different QOS strings in the created backup config")
    hostname = deepcopy(device['hostname'])
    # hostname = "LAB-ISR-092-01"
    createstringfiles = findstrings(hostname)
    # Check if the script has created both detected stringsfile and the running config
    # The order of how removing should follow his
    fnamecontrol = [
        "./playbooks/disconnect_servicepolicy.cfg",
        "./playbooks/policy_maps_detected.cfg",
        "./playbooks/class_maps_detected.cfg",
        "./playbooks/acl_detected.cfg",
        "./playbooks/new_qos_template.txt",
                    ]

    for i in fnamecontrol:
        if os.path.exists(i):
            print("Files exist: " + i)
        else:
            print("!-!-!-!-!-!-----Script Can't continue, problem with playbooks: " + i)
    #connecting to device again
    device = connecttodevice()
    device.open()
    for i in fnamecontrol:
        with open((i),"r") as file:
            playbook = file.read()
            device.load_merge_candidate(config = playbook)
            print("\n--------------------------Merging the configuration")
            print(f"\n--------------------------Make ready for pushing config from: {i}")
            print(device.compare_config())
            happy = input('Are You happy with this: [yes]') or yes
            if happy == 'yes':
                device.commit_config()
                print("\n--------------------------Pushing Config")
            else:
                device.discard_config()
                print("\n--------------------------Discarding Config")

    print(f"\n--------------------------Script has finished his job for {hostname}!")
    device.close()