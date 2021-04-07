import shutil
from copy import deepcopy

def copy_orig_file():
    src_site    = r"./templates/qos/pm_qos.cfg"
    dst_site    = r"./templates/qos/new_pm_qos.cfg"
    src_infra   = r"./templates/qos/central_infra_qos.cfg"
    dst_infra   = r"./templates/qos/new_central_infra_qos.cfg"
    shutil.copyfile(src_site, dst_site)
    shutil.copyfile(src_infra, dst_infra)

    return


def replacestrings_sites(dict_corp):
    dict_string = dict_corp

    # print(f"{dict_string}")
    dst = r"./templates/qos/new_pm_qos.cfg"
    # Calculate quickly a new variable : reason - the AAA-list-PM name is = AAA_QOS_5M_V-70-25-0-5 => replace "5M" value
    # i call this #M_id# and add it to the dictionary. => Higher then 10 is called FASTclient =>? ok
    download = str(dict_string.get("#DOWNLOAD#"))

    #Count the index of the string download - It works up unitl 1G connections!
    if len(download) <= 3:
        PM_ID = download[0:3]
        str_id = PM_ID + "K"
    elif len(download) <= 4:
        PM_ID = download[0]
        str_id = PM_ID + "M"
    elif len(download) <= 5:
        PM_ID = download[0:2]
        str_id = PM_ID + "M"
    else:
        PM_ID = download[0:3]
        str_id = PM_ID + "M"

    dict_string["#PM_ID#"] = str_id

    with open(dst, 'r') as file:
        filedata = file.read()

        # Replace the target string
        for key in dict_string.keys():
            filedata = filedata.upper().replace(key, str(dict_string[key]))
            # print(filedata)

        # Write the file out again
    with open(f"{dict_string['#SITE#']}_PM_QOS_{dict_string['#PM#']}.txt", "w") as file:
        file.write(filedata)


    dict_string_central_infra = deepcopy(dict_string)
    replacestrings_central_infra(dict_string_central_infra)

    return

def replacestrings_central_infra(dict_string_central_infra):
    dict_string = dict_string_central_infra
    #print(f"{dict_string}")
    dst = r"./templates/qos/new_central_infra_qos.cfg"
    with open(dst, 'r') as file:
        filedata = file.read()

        # Replace the target string
        for key in dict_string.keys():
            filedata = filedata.upper().replace(key, str(dict_string[key]))
            # print(filedata)

        # Write the file out again
    with open(f"C-INFRA_PM_QOS_{dict_string['#SITE#']}_{dict_string['#PM_ID#']}-{dict_string['#PM#']}.txt", "w") as file:
        file.write(filedata)


    dict_string_ikev2_prof = deepcopy(dict_string)
    prepare_ikev2_prof(dict_string_ikev2_prof)

    return

def prepare_ikev2_prof(dict_string_ikev2_prof):
    dict_string = dict_string_ikev2_prof
    # print(f"{dict_string}")
    dst = r"./templates/qos/SITE_IKEV2_PROFILE_NEW_PM.cfg"
    INT = input("New Ikev2 profile for what interface? => [G0|G1|G2]") or "G0"

    dict_string["#INT#"] = INT

    with open(dst, 'r') as file:
        filedata = file.read()

        # Replace the target string
        for key in dict_string.keys():
            filedata = filedata.upper().replace(key, str(dict_string[key]))
            # print(filedata)

        # Write the file out again
    with open(f"{dict_string['#SITE#']}_IKEV2_PROF_{dict_string['#INT#']}-{dict_string['#PM_ID#']}-{dict_string['#PM#']}.txt", "w") as file:
        file.write(filedata)


    return
