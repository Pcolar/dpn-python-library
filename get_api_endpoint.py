#!/usr/bin/python
""" Execution shell for DPN API get calls """

from app.dpn_python_library import *
import requests
import sys

def get_dpn_api(endpoint_string):
    """ Call service for dpn API  """
    dpn = {'url': 'http://ec2-54-226-144-188.compute-1.amazonaws.com'}
    dpn_headers={'Content-Type': 'application/json','Accept': 'application/json', 'Authorization': 'Token token=dpn_token'}
    # log_message("endpoint string: "+endpoint_string)
    if len(endpoint_string) is 0:
        log_message("Endpoint and query string is required")
        return -1
    else:
	# log_message("semding: " + dpn['url']+endpoint_string)
        response = requests.get(dpn['url']+endpoint_string, headers=dpn_headers)
        # log_message("Return code: " + str(response.status_code))
        print(response.text)
    return response.status_code

# Read content from stdin
dpn_querystring=sys.stdin.read().replace('\n', '')
# log_message("length of querystring input " + str(len(dpn_querystring)))
if len(dpn_querystring) is 0:
    exit(1)
if get_dpn_api(dpn_querystring) is 200:
    exit(0)
exit(1)

