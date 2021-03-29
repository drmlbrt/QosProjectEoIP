#Getting the partitioning for the different networks and their weights
pm= dict()
pm['corp']=input("What percentage Corporate? :") or 50
pm['scnet']=input("What percentage SecNet? :") or 25
pm['pbnet']=input("What percentage PubNet? :") or 25

serveronboard=input("Is there a server on board?: True or False? = ") or True
#Print out the selection and check if total = 100%
for key, value in pm.items():
    print(f"{key:16s} : {value}")
total=int(pm['corp'])+int(pm['scnet'])+int(pm['pbnet'])
if total == 100 :
    print("Perfect choice")
    print(f"the new PM is: PM_QOS_C_V-{pm['corp']}-{pm['scnet']}-0-{pm['pbnet']}")
else:
    print("Given values are not equal to 100%")
    print("Go start again and give correct information please.")

