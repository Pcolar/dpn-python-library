#!/usr/bin/python

import requests
import sys
import os
from dpn_python_library import *

# Creates a bag entry in the DPN architecture via the DPN API
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

endpoint = {'bag': '/api-v2/bag', 'member': '/api-v2/member', 'node': '/api-v2/node', 'repl': '/api-v2/replicate'}

# Read content from stdin
dpn_bag=sys.stdin.read().replace('\n', '')
# log_message("length of JSON input " + str(len(dpn_bag)))
if len(dpn_bag) is 0:
    exit(1)

#log_message(dpn_headers)
#log_message(dpn_bag)

response = requests.post(dpn_host+endpoint['bag'], headers=dpn_headers, data=dpn_bag)
log_message("Return code: " + str(response.status_code))
log_message(response.text)

if  response.status_code is 201:
    exit(0)
exit(1)
