textstrings = {'#PM#': 'V-25-25-25-25',
               '#SRV#': 4,
               '#TRANSACT#': 5,
               '#INTERACT#': 7,
               '#BULK#': 1,
               '#PRIORITY#': 7,
               '#PUBNET#': 24,
               '#BUISNET#': 24,
               '#HIGHNET#': 24,
               '#ROUTING#': 1,
               '#NETMGT#': 1,
               '#CALLSIG#': 1,
               '#DEFAULT#': 1,
               '#VOICE#': 15,
               '#VIDEO#': 10,
               '#UPLOAD#': 1024,
               '#DOWNLOAD#': 120000}

download = str(textstrings.get("#DOWNLOAD#"))
print(len(download))

if len(download) <= 3:
    PM_ID = download[0:3]
    str_id = PM_ID + "K"
elif len(download) <= 4:
    PM_ID = download[0]
    str_id= PM_ID + "M"
elif len(download) <= 5:
    PM_ID = download[0:2]
    str_id = PM_ID + "M"
else:
    PM_ID = download[0:3]
    str_id = PM_ID + "M"

print(str_id)
