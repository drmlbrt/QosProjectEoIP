from DEV.m02_PlanePython.utils.napalmconnect import connecttodevice

if __name__ == '__main__':
    print("\n-------------------Connecting to devices configured in the connect! Verify this before")
    device = connecttodevice()
    device.open()
    commands = ["show policy-map interface tu11 | i Service-policy : "]
    policy_map = device.cli(commands)
    print("\n---------- Presenting you the running policy-map on Tu11")
    for value in policy_map.values():
        clean = [item.strip() for item in value.split(':')]
        with open(f"./playbooks/policy_map_" + clean[1] + ".cfg", "w+") as file:
            pm = ["show run | s policy-map " + clean[1]]
            pm_result = device.cli(pm)
            for value in pm_result.values():
                print(value)
                file.write(value)
                file.close()
    print("\n---------- What would you like to change?")
    print("\n|------ For simplicity change the  values in the file, then run part 2")
    with open(f"./playbooks/policy_map_" + clean[1] + ".cfg", "w+") as file:
