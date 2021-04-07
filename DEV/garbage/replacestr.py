
from time import time

import shutil
import os
import re


dict_string = {'SRV': 10, 'TRANSACT': 13, 'INTERACT': 20, 'BULK': 3, 'PRIORITY': 20, 'PUBNET': 5, 'BUISNET': 0, 'HIGHNET': 24}
text_str = """
policy-map PM_QOS_C_#PM#
 class CM_QOS_C_VOICE
  priority level 1
  police cir percent #VOICE#
 class CM_QOS_C_VIDEO
  priority level 2 percent #VIDEO#
  police cir percent 30
 class CM_QOS_C_ROUTING
  bandwidth remaining percent #ROUTING#
  police cir percent 6
 class CM_QOS_C_NETMGT
  bandwidth remaining percent #NETMGT#
  police cir percent 6
  set mpls experimental topmost 7
 class CM_QOS_C_CALLSIG
  bandwidth remaining percent #CALLSIG#
  set mpls experimental topmost 7
  police cir percent 6
 class CM_QOS_C_SRV
  bandwidth remaining percent #SRV#
  queue-limit 4096 packets
  police cir percent 40
 class CM_QOS_C_PRIORITY
  bandwidth remaining percent #PRIORITY#
  queue-limit 64 packets
  police cir percent 50
 class CM_QOS_C_INTERACT
  bandwidth remaining percent #INTERACT#
  random-detect dscp-based
  random-detect dscp 26 32 40 10
  queue-limit 128 packets
  police cir percent 50
 class CM_QOS_C_TRANSACT
  bandwidth remaining percent #TRANSACT#
  police cir percent 50
   service-policy PM_QOS_C_PROXY
 class CM_QOS_C_BULK
  bandwidth remaining percent #BULK#
  random-detect dscp-based
  police cir percent 50
 class CM_QOS_C_HIGHNET
  bandwidth remaining percent #HIGHNET#
  random-detect dscp-based
  police cir percent 15
 class CM_QOS_C_BUISNET
  random-detect dscp-based
  police cir percent #BUISNET#
 class CM_QOS_C_PUBNET
  bandwidth remaining percent #PUBNET#
  fair-queue
  random-detect
  random-detect precedence 0 2 32 2
  random-detect precedence 1 5 32 3
  random-detect precedence 2 10 32 4
  random-detect precedence 3 20 32 4
  police cir percent 30
   exceed-action set-mpls-exp-topmost-transmit 1
   violate-action drop
 class CM_QOS_C_DEFAULT
  bandwidth remaining percent #DEFAULT#
  fair-queue
  random-detect
  random-detect precedence 0 1 28 1
  police cir percent 10
 class class-default
  fair-queue
  random-detect
  police cir percent 3
!
!
"""
dict_string = {'#SRV#': 10, '#TRANSACT#': 13, '#INTERACT#': 20, '#BULK#': 3, '#PRIORITY#': 20, '#PUBNET#': 5, '#BUISNET#': 0, '#HIGHNET#': 24}
# qos_dictv={ "#SRV#": ,
#             "#PRIORITY#": ,
#             "#INTERACT#": ,
#             "#TRANSACT#": ,
#             "#BULK#": ,
#             "#HIGHNET#": ,
#             "#PUBNET#": ,
# }
print(f"{dict_string}")

for key in dict_string.keys():
    text_str = text_str.upper().replace(key, str(dict_string[key]))
print(text_str)
