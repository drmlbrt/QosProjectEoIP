import requests
from requests.auth import HTTPBasicAuth

# Disable SSL Verification Warning because of Private SSL Certificate

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AUTH = HTTPBasicAuth("hannibal", "hannibal")
MEDIA_TYPE = "application/yang-data+json"
HEADERS = {"Accept": MEDIA_TYPE,
           "Content-Type": MEDIA_TYPE}

url = "https://10.242.1.92/restconf/data/Cisco-IOS-XE-native:native/interface"

response = requests.get(url=url, auth=AUTH, headers=HEADERS, verify=False)

print("API: ", url)

print(response.status_code)

if response.status_code in [200, 202, 204]:
    print("Successful")
else:
    print("Error in API Request")

print(response.text)
print("="*40)
print("="*40)
