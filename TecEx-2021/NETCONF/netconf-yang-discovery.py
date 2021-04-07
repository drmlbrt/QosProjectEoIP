from ncclient import manager
import xmltodict
import xml.dom.minidom

# Create an XML filter for targeted NETCONF queries

with manager.connect(
         host="10.242.1.92",
         port="830",
         username="hannibal",
         password="hannibal",
         hostkey_verify=False
         ) as m:

    netconf_reply = m.get(filter=('xpath' ,
        "/interfaces-state/interface[name='GigabitEthernet0/0/1']"
        "/statistics/out-unicast-pkts"))

    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    # Parse the returned XML to an Ordered Dictionary
    intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]


    # Create a list of interfaces
    intf_info = intf_details["interfaces-state"]["interface"]

    print("")
    print("Interface Details:")
    print(" Name: {}".format(intf_info["name"]))
    print(" Packets Output: {}".format(intf_info["statistics"]["out-unicast-pkts"]))
