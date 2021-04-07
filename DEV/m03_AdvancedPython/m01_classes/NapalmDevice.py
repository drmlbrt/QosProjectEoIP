from Device import Device

import napalm

# NOTE: this will disable insecure HTTPS request warnings that NAPALM gets
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from update_qos import *

class NapalmDevice(Device):

    def connect(self):
        # Use the appropriate network driver to connect to the device:
        driver = napalm.get_network_driver(self.device_type)

        # Connect:
        self.connection = driver(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            optional_args={"global_delay_factor": 2}
        )
        print(f"----- Connecting to {self.hostname}")
        self.connection.open()
        print(f"----- Connected ! ")

        return True

    def get_facts(self):
        return self.connection.get_facts()

    def get_running(self):
        print(f"----- Downloading running cfg from {self.hostname}! ")
        backup = self.connection.get_config()["running"]
        with open(f"../backup_runcfg/{self.name}.cfg", "w+") as file:
            file.write(backup)
            file.close()
        return backup

    def disconnect(self):
        print(f"----- Disconnected from {self.hostname}")
        return self.connection.close()
