import json
import pprint
import xmltodict


f = open("data.json")
data = json.load(f)

print(json.dumps(data, sort_keys=True, indent=4 ))

with open("json_to.xml", "w") as xmlout:
    xmlout.write(xmltodict.unparse(data, pretty=True))
