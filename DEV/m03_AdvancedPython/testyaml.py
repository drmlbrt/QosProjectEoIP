import yaml
from pprint import pprint
print("\n-----Printing the contents of a yaml File\t")

with open("playbooks/devices.yaml", "r") as readfile:
    yaml_inventory = readfile.read()
    print(yaml.dump(yaml.safe_load(yaml_inventory), indent=4))
    readfile.close()

with open("playbooks/devices.yaml", "r") as file:
    yamldict = yaml.full_load(file)
    print("\n-----Printing the contents of a yaml full load")
    print(yamldict)

    print("\n-----Printing the contents of a yaml devices value 'list'")
    print(f"{yamldict['devices']}")

    print("\n-----Pretty Printing the contents of a yaml File")
    pprint(f"{yamldict['devices']}")

    print("\n-----Creating a list of dictionaries")
    # for value in yamldict.values():
    #     deviceslist = value
    #     print(deviceslist)
    #     print("\n-----Printing the key value")
    #     for item in deviceslist:
    #         print(f"\n")
    #         print(item)
    for device in yamldict.values():
        print(device)

    file.close()