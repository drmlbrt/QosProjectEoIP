from __future__ import division

def pm_qos_calculate(vc=15, vi=10, corp=70, sec=20, bus=0, pub=10):
    #Standard config templated with video and voice fixed values
    voice = vc
    video = vi
    prc_voice= int(voice)
    prc_video= int(video)
    total= 100
    rest_1= round(float(total - prc_voice - prc_video))

    # print(f"Rest1: {rest_1}%")
    #The partitioning of the CORP/PUBNET/HIGHNET/OTHER is again 100% - Remaining percentage in config
    #First The common factors=
    Common =   1
    CommonDict= {"Routing"      : Common,
                 "NetworkMgt"   : Common,
                 "CallSig"      : Common,
                 "Default"      : Common,
                 }
    # print(sum(CommonDict.values()))

    rest_2 = round(float(total - sum(CommonDict.values())))
    # print(f"Rest2: {rest_2}%")
    #Calculating the reamaing values
    corporate   = corp
    pubnet      = pub
    highnet     = sec
    buisnet     = bus
    Eoip_Qos={"Corporate":corporate,
              "Pubnet":pubnet,
              "Highnet":highnet,
              "Buisnet":buisnet,
              }
    corp_weight={"corp_srv"  : 0,
                 "corp_trans": 30,
                 "corp_int"  : 30,
                 "corp_bulk" : 10,
                 "corp_prio" : 30,
                 }
    if sum(corp_weight.values()) == 100:
        dict_corp_val = dict()
        # print("The Corporate values are correct")
        srv   =  round((((rest_2)/100)*((Eoip_Qos["Corporate"])/100)*((corp_weight["corp_srv"])/100))*100)
        # print(f"SRV: {srv}%")
        dict_corp_val["SRV"]= srv
        trans = round((((rest_2)/100)*((Eoip_Qos["Corporate"])/100)*((corp_weight["corp_trans"])/100))*100)
        # print(f"TRANSACT: {trans}%")
        dict_corp_val["TRANSACT"]= trans
        inter   = round((((rest_2)/100)*((Eoip_Qos["Corporate"])/100)*((corp_weight["corp_int"])/100))*100)
        # print(f"INTERACT: {int}%")
        dict_corp_val["INTERACT"]=inter
        bulk  = round((((rest_2)/100)*((Eoip_Qos["Corporate"])/100)*((corp_weight["corp_bulk"])/100))*100)
        # print(f"BULK: {bulk}%")
        dict_corp_val["BULK"]=bulk
        prio  = round((((rest_2)/100)*((Eoip_Qos["Corporate"])/100)*((corp_weight["corp_prio"])/100))*100)
        # print(f"PRIORITY: {prio}%")
        dict_corp_val["PRIORITY"]=prio
        pub   = round((((rest_2)/100)*((Eoip_Qos["Pubnet"])/100)*100))
        # print(f"PUBNET: {pub}%")
        dict_corp_val["PUBNET"]=pub
        buis  = round((((rest_2)/100)*((Eoip_Qos["Buisnet"])/100)*100))
        # print(f"BUISNET: {buis}%")
        dict_corp_val["BUISNET"]=buis
        high  = round((((rest_2)/100)*((Eoip_Qos["Highnet"])/100)*100))
        # print(f"HIGHNET: {high}%")
        dict_corp_val["HIGHNET"]=high
        for key, value in dict_corp_val.items():
            print(f"{key:10s} : {value:2} %")
        remainingtotal= (sum(dict_corp_val.values())) + (sum(CommonDict.values()))
        print(f"{remainingtotal}% (Includes the common values !")
    else:
        print("The values are not correct for corporate")

    return dict_corp_val

def create_pm_file():
    return




