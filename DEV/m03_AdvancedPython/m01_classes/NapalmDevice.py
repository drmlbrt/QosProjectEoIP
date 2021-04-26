from Device import Device

import napalm

# NOTE: this will disable insecure HTTPS request warnings that NAPALM gets
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        return self.connection.close()

    def load_config(self, playbookqostemplate):
        self.playbookqostemplate=playbookqostemplate
        return self.connection.load_merge_candidate(config=self.playbookqostemplate)

    def compare_config(self):
        return self.connection.compare_config()

    def commit_config(self):
        return self.connection.commit_config()

    def discard_config(self):
        return self.connection.discard_config()

    def clicmd(self, commands):
        self.commands = commands
        return self.connection.cli(self.commands)