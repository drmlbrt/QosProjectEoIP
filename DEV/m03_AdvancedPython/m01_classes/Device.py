"""
Here we define the Device Class, this is the common device information we should use to connect to a device.
"""
from update_qos import *

class Device:

    def __init__(self, name, hostname, device_type):
        self.name = name
        self.hostname = hostname
        self.device_type = device_type

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def set_port(self, port):
        self.port = port

    def connect(self):
        raise NotImplementedError("Please Implement the connect() method")

    def get_facts(self):
        raise NotImplementedError("Please Implement the get_facts() method")

    def get_running(self):
        raise NotImplementedError("Please Implement the get_running() method")

    def disconnect(self):
        raise NotImplementedError("Please Implement the disconnect() method")

    def findqosstrings(self):
        self.findqosstrings = findqosstrings(self.name)
        return findqosstrings

    def update_qos_template(self):
        self.update_qos_template = update_qos_template(self.name)

