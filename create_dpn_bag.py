__copyright__ = "Copyright (C) 2017 Digital Preservation Network, LLC"
__license__ = "BSD Version 3 License"

import json
import requests
import datetime
import sys
import os
from dpn_python_library import *

""" Creates a bag entry in the DPN architecture via the DPN API """
###  Requires a json file with the bag data

if  "dpn_host" in os.environ:
    dpn_host = os.environ['dpn_host']
else:
    log_message("Expecting: dpn_host, dpn_token")
    exit(1)
if  "dpn_token" in os.environ:
    token = os.environ['dpn_token']
else:
    log_message("Expecting: dpn_host, dpn_token")
    exit(1)
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json'}
dpn_headers['Authorization']="Token token="+token
#log_message("DPN Host: "+dpn_host)
#log_message("DPN Headers: "+json.dumps(dpn_headers))

# Read command line parameters
try:
    if  sys.argv[1:] is "":
        log_message("A DPN bag metadata file in json format must be specified" )
        exit(1)
    else:
        infile = str(sys.argv[1])

    with open(infile, 'r') as json_data:
        dpn_bag=json_data.read().replace('\n', '')
except:
    log_message("A DPN bag metadata file in json format must be specified" )
    exit(1)

response = requests.post(dpn_host+"/api-v2/bag", headers=dpn_headers, data=dpn_bag)
log_message("Return code: " + str(response.status_code))
log_message(response.text)

if  response.status_code is 201:
    exit(0)
exit(1)
