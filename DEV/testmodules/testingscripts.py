dict_of_strings = {
                    "policy_maps" : ["policy-map PM_QOS_"],
                    "class_maps" : ["class-map match-any CM_QOS_","class-map match-all CM_QOS_"],
                    "acl" : ["ip access-list extended ACL_QOS", "ip access-list extended ACL_IP"]
                   }

configfile= """
policy-map PM_QOS_C_V-50-0-50-0
policy-map PM_QOS_C_V-50-0-50-1
policy-map PM_QOS_C_V-50-0-50-2
policy-map PM_QOS_C_V-50-0-50-3
ip access-list extended ACL_IP_01
ip access-list extended ACL_IP_02
ip access-list extended ACL_IP_03
ip access-list extended ACL_IP_04
class-map match-all CM_QOS_01
class-map match-all CM_QOS_02
class-map match-all CM_QOS_03
ip access-list extended ACL_QOS_01
ip access-list extended ACL_QOS_02
ip access-list extended ACL_QOS_03
ip access-list extended ACL_QOS_03
"""
linenum = 0


for k,v in dict_of_strings.items():
    with open("./TEST_" + k + ".cfg", "a+") as file:
        print(v)
    file.close()


with open(f"./backup_runcfg/LAB-ISR-092-01.cfg","rt") as myfile:
    for line in myfile:
        linenum += 1
        if line.find("QOS") != -1:
            for k, v in dict_of_strings.items():
                with open("./TEST_" + k + ".cfg", "a+") as file:
                    for item in v:
                        if item in line:
                            file.write("no " + line )
                            print(line)
                file.close()
myfile.close()