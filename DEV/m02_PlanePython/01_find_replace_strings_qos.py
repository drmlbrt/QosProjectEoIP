# goal is a total cleanup of all existing configuration qos and replace with basic EoIP template
# only to replace the OUTGOING policy-maps -> find string policy-map PM_QOS_C]
# the script does not touch the existing class-maps as they do generally not change.
# The basic PM_QOS_C_100-0-0-0 will be copied.

#####OLD FILE TEST SCRIPT ONLY#######
linenum = 0
list_of_strings = ["policy-map PM_QOS_C"]
list_of_strings_2 = ["class-map match-any CM_QOS_C"]
hostname = 'LAB-ISR-092-01'
with open("./playbooks/policy-maps_detected.cfg", "w+") as qosfile:
    print("\n----- Trying to find the class-map on Physical G0/G1/G2 -----------------------------")
    with open(f"./backup_runcfg/{hostname}.cfg","rt") as myfile:
        print("\nSearching for string QOS in running config file")
        for line in myfile:
            linenum += 1
            if line.find("QOS") != -1:
                for string_to_search in list_of_strings:
                    if string_to_search in line:
                        print(line)
                        qosfile.write("no "+line)
    myfile.close()
qosfile.close()

with open("playbooks/class-maps_detected.cfg", "w+") as cm_qosfile:
    print("\n----- Trying to find the policy-map on router type 'C' -----------------------------")
    with open(f"./backup_runcfg/{hostname}.cfg","rt") as myfile:
        print("\nSearching for string QOS in running config file")
        for line in myfile:
            linenum += 1
            if line.find("QOS") != -1:
                for string_to_search in list_of_strings_2:
                    if string_to_search in line:
                        print(line)
                        cm_qosfile.write("no "+line)
    myfile.close()
cm_qosfile.close()








