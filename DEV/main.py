# This is a Python script.
# The script creates and automate QoS Policy MAPS for Sites
# 2021 01 21 Lt DERMUL Bart - EoIP - Project KAKAPO.
from DEV.garbage.Utils.utils import *

if __name__ == '__main__':
    pm_values = dict()
    print("|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|")
    print("Welcome to the QoS - Policy Map creation script")
    print("read carefully your SATLINK operator card")
    print("Example: VOICE:Fixed%, VIDEO:Fixed%, SERVER: YES/NO, CORP-SECNET-OTHER-PUBNET[70-20-0-10]")

    print("|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|")
    print("|---------------------------------------------------------|")
    create_pm = input_req()



