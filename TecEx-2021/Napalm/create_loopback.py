from napalm import get_network_driver
import copy

print("\nThis is the playbook contents -----------------------------------")
with open("./playbooks/create_loopback.txt", "r") as file:
    playbook = file.read()
    print(playbook)

driver = get_network_driver("ios")
#Error with IOS 15 - solved with optional arguments src: GitHub support pages
device = driver("10.242.1.92", "hannibal", "hannibal", optional_args={"global_delay_factor":2})
print("\nConnecting to device        -------------------------------------")
device.open()
device.load_merge_candidate(config = playbook)
print("\nMerging the configuration        --------------------------------")
print("\nPrinting the new device config 'again' --------------------------")
print(device.compare_config())
happy = input('Are You happy with this: [yes]') or yes
if happy == 'yes' :
    device.commit_config()
    print("\nPushing Config          ------------------------------------")
else:
    device.discard_config()
    print("\nDiscarding Config       ------------------------------------")

device.close()
