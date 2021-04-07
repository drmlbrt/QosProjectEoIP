import os.path

def findqosstrings(name):
    """
    This part will search on a fixed string dictionary. the keys are important in the order. they create the
    files that we need to 'delete' the current QOS CLI on the router. You can manually add values to it.
    """
    linenum = 0
    dict_of_strings = {"policy_maps": ["policy-map PM_QOS_"],
                       "class_maps": ["class-map match-any CM_QOS_",
                                      "class-map match-all CM_QOS_"],
                       "acl": ["ip access-list extended ACL_QOS",
                               "ip access-list extended ACL_IP"]}

    print(f"\n----- Looping through strings to find for {name}")
    with open(f"../backup_runcfg/{name}.cfg", "rt") as myfile:
        for line in myfile:
            linenum += 1
            if line.find("QOS") != -1:
                for k, v in dict_of_strings.items():
                    with open("../playbooks/" + k + "_detected.cfg", "a+") as file:
                        for item in v:
                            if item in line:
                                file.write("no " + line)
                                print(line)
                    file.close()
    print(f"\n----- Searching QOS Strings is finished for {name}")
    myfile.close()
    return True

def update_qos_template(name):
        findqosstrings(name)

        # Check if the script has created both detected stringsfile and the running config
        # The order of how removing should follow this or you break the working of the Update! Probably could order this with a dict?

        fnamecontrol = [
            "../playbooks/disconnect_servicepolicy.cfg",
            "../playbooks/policy_maps_detected.cfg",
            "../playbooks/class_maps_detected.cfg",
            "../playbooks/acl_detected.cfg",
            "../playbooks/new_qos_template.txt",
                        ]

        for i in fnamecontrol:
            if os.path.exists(i):
                print("Files exist: " + i)
            else:
                print("!-!-!-!-!-!-----Script Can't continue, problem with playbooks: " + i)
        #connecting to device again
        for i in fnamecontrol:
            with open(i, "r") as file:
                playbook = file.read()
                device.load_merge_candidate(config=playbook)
                print("\n----- Merging the configuration")
                print(f"\n----- Make ready for pushing config from: {i}")
                print(device.compare_config())
                happy = input('Are You happy with this: [yes]') or yes
                if happy == 'yes':
                    device.commit_config()
                    print("\n----- Pushing Config")
                else:
                    device.discard_config()
                    print("\n----- Discarding Config")

        print(f"\n----- Script has finished his job for {name}!")

