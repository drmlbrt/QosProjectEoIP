import xmltodict
import json
import pprint

with open("xml-file.xml") as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()

    json_data=json.dumps(data_dict, sort_keys=True, indent=4)
    print(json_data)
    with open("data.json", "w") as json_file:
        json_file.write(json_data)
        json_file.close()