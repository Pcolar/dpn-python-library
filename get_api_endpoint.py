#!/usr/bin/python
""" DPN API call shell """

from app.dpn_python_library import *
import requests
import sys
import os

def get_dpn_api(url, token, endpoint_string):
    """ Call service for dpn API  """
    dpn = {'url': url}
    dpn_headers={'Content-Type': 'application/json','Accept': 'application/json'}
    dpn_headers['Authorization']="Token token="+token
    if len(endpoint_string) is 0:
        log_message("Endpoint and query string is required")
        return -1
    else:
	#log_message("sending: " + dpn['url']+endpoint_string)
        #print dpn_headers
        response = requests.get(dpn['url']+endpoint_string, headers=dpn_headers)
        # log_message("Return code: " + str(response.status_code))
        print(response.text)
    return response.status_code

# Retrieve environment variables
if  "dpn_host" in os.environ:
    dpn_host = os.environ['dpn_host']
else:
    log_message("Expecting: dpn_host")
    exit(1)
if  "dpn_token" in os.environ:
    dpn_token = os.environ['dpn_token']
else:
    log_message("Expecting: dpn_token")
    exit(1)
#log_message("DPN Host: "+dpn_host)
#log_message("DPN Headers: "+json.dumps(dpn_headers))

# Read content from stdin
dpn_querystring=sys.stdin.read().replace('\n', '')
# log_message("length of querystring input " + str(len(dpn_querystring)))
if len(dpn_querystring) is 0:
    exit(1)
if get_dpn_api(dpn_host, dpn_token, dpn_querystring) is 200:
    exit(0)
exit(1)

