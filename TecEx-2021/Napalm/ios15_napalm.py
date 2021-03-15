from napalm import get_network_driver
import json

driver = get_network_driver("ios")
#Error with IOS 15 - solved with optional arguments src: GitHub support pages
device = driver("10.242.1.***", "******", "******", optional_args={"global_delay_factor":2})
device.open()
print(device.get_config()["running"])
device.close()