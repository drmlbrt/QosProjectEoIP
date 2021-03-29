from copy import deepcopy

def pm_qos_calc(vc, vi, corp, sec, bus, pub, srv, upl=1024, dwnl=1024):
    dict_corp_val = dict()

    #Standard config templated with video and voice fixed values
    prc_voice= int(vc)
    prc_video= int(vi)
    total= 100
    rest_1  = (total - prc_voice - prc_video)
    dict_voice_video = {"#VOICE#": prc_voice , "#VIDEO#": prc_video,}
    upload = int(upl)
    download= int(dwnl)
    dict_upl_dwnl = {"#UPLOAD#": upload , "#DOWNLOAD#": download,}

    # print(f"Rest1: {rest_1}%")
    #The partitioning of the CORP/PUBNET/HIGHNET/OTHER is again 100% - Remaining percentage in config
    #First The common factors=
    Common =   1
    CommonDict= {"#ROUTING#"      : Common,
                 "#NETMGT#"       : Common,
                 "#CALLSIG#"      : Common,
                 "#DEFAULT#"      : Common,
                 }
    # print(sum(CommonDict.values()))

    rest_2 = total - sum(CommonDict.values())

    #Calculating the reamaing values
    # corporate   = corp
    # pubnet      = pub
    # highnet     = sec
    # buisnet     = bus
    Eoip_Qos={"Corporate": int(corp),
              "Pubnet":    int(pub),
              "Highnet":   int(sec),
              "Buisnet":   int(bus),
              }
    corp_weight = dict()
    # the string #PM# e.g: POLICY-MAP PM_QOS_C_"V-70-20-0-10"
    #replacing PM_QOS_C_#PM#
    if vi == 0:

        dict_corp_val["#PM#"]=str(
            f"NV-{Eoip_Qos['Corporate']}-{Eoip_Qos['Highnet']}-{Eoip_Qos['Buisnet']}-{Eoip_Qos['Pubnet']}")
    else:
        dict_corp_val["#PM#"] = str(
            f"V-{Eoip_Qos['Corporate']}-{Eoip_Qos['Highnet']}-{Eoip_Qos['Buisnet']}-{Eoip_Qos['Pubnet']}")
    # etermine your 'weight' this is fixed in the script, can be automated
    if srv == True:
        corp_weight["corp_srv"]   = 15
        corp_weight["corp_trans"] = 20
        corp_weight["corp_int"]   = 30
        corp_weight["corp_bulk"]  = 5
        corp_weight["corp_prio"]  = 30
    else:
        corp_weight["corp_srv"]   = 0
        corp_weight["corp_trans"] = 20
        corp_weight["corp_int"]   = 45
        corp_weight["corp_bulk"]  = 5
        corp_weight["corp_prio"]  = 30

    if sum(corp_weight.values()) == 100:

        # print("The Corporate values are correct")
        srv   =  round(((float(rest_2)/100)*(float(Eoip_Qos["Corporate"])/100)*(float(corp_weight["corp_srv"])/100))*100)
        # print(f"SRV: {srv}%")
        dict_corp_val["#SRV#"]= int(srv)
        trans = round(((float(rest_2)/100)*(float(Eoip_Qos["Corporate"])/100)*(float(corp_weight["corp_trans"])/100))*100)
        # print(f"TRANSACT: {trans}%")
        dict_corp_val["#TRANSACT#"]= int(trans)
        inter   = round(((float(rest_2)/100)*(float(Eoip_Qos["Corporate"])/100)*(float(corp_weight["corp_int"])/100))*100)
        # print(f"INTERACT: {int}%")
        dict_corp_val["#INTERACT#"]= int(inter)
        bulk  = round(((float(rest_2)/100)*(float(Eoip_Qos["Corporate"])/100)*(float(corp_weight["corp_bulk"])/100))*100)
        # print(f"BULK: {bulk}%")
        dict_corp_val["#BULK#"]= int(bulk)
        prio  = round(((float(rest_2)/100)*(float(Eoip_Qos["Corporate"])/100)*(float(corp_weight["corp_prio"])/100))*100)
        # print(f"PRIORITY: {prio}%")
        dict_corp_val["#PRIORITY#"]= int(prio)
        pub   = round(((float(rest_2)/100)*(float(Eoip_Qos["Pubnet"])/100)*100))
        # print(f"PUBNET: {pub}%")
        dict_corp_val["#PUBNET#"] = int(pub)
        buis  = round(((float(rest_2)/100)*(float(Eoip_Qos["Buisnet"])/100)*100))
        # print(f"BUISNET: {buis}%")
        dict_corp_val["#BUISNET#"] = int(buis)
        high  = round(((float(rest_2)/100)*(float(Eoip_Qos["Highnet"])/100)*100))
        # print(f"HIGHNET: {high}%")
        dict_corp_val["#HIGHNET#"] = int(high)


        for key, value in dict_corp_val.items():
            print(f"{key:10s} : {value:2} %")

        test = deepcopy(dict_corp_val)
        print(test)
        test.pop("#PM#")
        print(test)






        # sumtest1 = sum(dict_corp_val.values())
        #
        # print(totalstest1)
        #
        # # if totalstest1 != 100 :
        # #     print("Added 1% to BULK to avoid calculation rounding issue!")
        # #     dict_corp_val["#BULK#"] = str(dict_corp_val["#BULK#"] + 1)
        # # else:
        # #     remainingtotal=(sum(dict_corp_val.values())) + (sum(CommonDict.values()))
        # #
        # # #Howtosolve this? -Rounding issues
        # #     print(f"{remainingtotal}% (Includes the common values !) When 99% 'rounding issues' just add 1% somewhere'")

    else:

        print("The values are not correct for corporate")

    dict_corp = {**dict_corp_val, **CommonDict, **dict_voice_video, **dict_upl_dwnl}




    createnew = input("Generate a new PM FILE?: [Y|N]") or "Y"

    if createnew.lower() == "y":
        replacestrings(dict_corp)

        print("Calculating Real upload and download values")
        #calc_final_perc(dict_corp)
    else:
        print("Thank you for participating")
    return



pm_values = dict()

print("----------------------------------------------------------")
print("\n-Please provide bandwidth--------------------------------")
upload = input("Upload speed in kbps [def:1024]: ") or 1024
pm_values["Upload"] = int(upload)
download = input("Download speed in kbps [def:1024]: ") or 1024
pm_values["Download"] = int(download)

print("----------------------------------------------------------")
print("\n---------Change Voice/Video values---------")
fixed = input("Keep default values for VOICE[9%]/VIDEO[15%] [Y/N]: ") or 'Y'
if fixed.lower() == 'y':
    vid = int(10)
    voice = int(15)
    pm_values["VIDEO"] = vid
    pm_values["VOICE"] = voice
else:
    vid = input("New VIDEO value: ") or 15
    vc = input("New VOICE value: ") or 9
    pm_values["VIDEO"] = int(vid)
    pm_values["VOICE"] = int(voice)

print("----------------------------------------------------------")
print("\n---------With Deployed Server or not?---------")
serverdeployed = input("Will there be a server on board? [Y/N]: ") or 'Y'

if serverdeployed.lower() == 'y':
    srv = True
    pm_values["SERVER"] = srv
else:
    srv = False
    pm_values["SERVER"] = srv

print("---------------------------------------------------------")
print("\n--------Provide Now Values for BW-partitioning?---------")
print("---------|CORP|-|SECNET|-|OTHER|-|PUBNET|----------------")
print("---------|%|----|%|------|%|-----|%|---------------------")
print("----DEF:-|25|---|25|-----|25|----|25|--------------------")
corp = input("Reserved BW for CORPNET: ") or 25
secnet = input("Reserved BW for SECNET: ") or 25
other = input("Reserved BW for OTHER: ") or 25
pubnet = input("Reserved BW for PUBNET: ") or 25
pm_values["CORPNET"] = corp
pm_values["SECNET"] = secnet
pm_values["OTHER"] = other
pm_values["PUBNET"] = pubnet

pm_qos_calc( vc=    pm_values["VOICE"],
             vi=    pm_values["VIDEO"],
             corp=  pm_values["CORPNET"],
             sec=   pm_values["SECNET"],
             bus=   pm_values["OTHER"],
             pub=   pm_values["PUBNET"],
             srv=   pm_values["SERVER"],
             upl=   pm_values["Upload"],
             dwnl=  pm_values["Download"])

