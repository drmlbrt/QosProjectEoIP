def findstrings(hostname):
    linenum = 0
    dict_of_strings = {"policy_maps" : ["policy-map PM_QOS_"],
                       "class_maps" : ["class-map match-any CM_QOS_",
                       "class-map match-all CM_QOS_"],
                      "acl" :["ip access-list extended ACL_QOS",
                       "ip access-list extended ACL_IP"]}


    print(f"\n--------------- Looping through strings to find for  {hostname}")
    with open(f"./backup_runcfg/{hostname}.cfg","rt") as myfile:
        for line in myfile:
            linenum += 1
            if line.find("QOS") != -1:
                for k, v in dict_of_strings.items():
                    with open("./playbooks/" + k + "_detected.cfg", "a+") as file:
                        for item in v:
                            if item in line:
                                file.write("no " + line)
                                print(line)
                    file.close()
    myfile.close()