#!/usr/bin/python
import json
import requests
import datetime
import sys
import os

def log_message(message):
    """print out  in log message format"""
    print "%s:  %s" % (datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), message)

""" Creates a bag entry in the DPN architecture via the DPN API """
###  Requires a json file with the bag data

dpn = {'url': 'http://ec2-54-226-144-188.compute-1.amazonaws.com', 'token': 'dpn_token'}
endpoint = {'bag': '/api-v2/bag', 'member': '/api-v2/member', 'node': '/api-v2/node', 'repl': '/api-v2/replicate'}
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json', 'Authorization': 'Token token=dpn_token'}

# Read content from stdin
dpn_bag=sys.stdin.read().replace('\n', '')
# log_message("length of JSON input " + str(len(dpn_bag)))
if len(dpn_bag) is 0:
    exit(1)

#log_message(dpn_headers)
#log_message(dpn_bag)

response = requests.post(dpn['url']+endpoint['bag'], headers=dpn_headers, data=dpn_bag)
log_message("Return code: " + str(response.status_code))
log_message(response.text)

if  response.status_code is 201:
    exit(0)
exit(1)

