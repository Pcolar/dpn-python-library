#!/usr/bin/python
""" DPN API call shell """

from app.dpn_python_library import *
import requests
import sys

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
dpn_host, dpn_token = load_environment()
# log_message("DPN Host: "+dpn_host+" DPN Token: "+dpn_token)
# log_message("DPN Headers: "+json.dumps(dpn_headers))

# Read content from stdin
dpn_querystring=sys.stdin.read().replace('\n', '')
if len(dpn_querystring) is 0:
    log_message("length of querystring: " + str(len(dpn_querystring)))
    exit(1)
if get_dpn_api(dpn_host, dpn_token, dpn_querystring) is 200:
    exit(0)
# fallthrough
exit(1)

