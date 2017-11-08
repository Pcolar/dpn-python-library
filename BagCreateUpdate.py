#!/usr/bin/python
""" DPN API GET and POST calls to update a registry bag record """

from app.dpn_python_library import *
import json
import requests
import datetime
import sys
import os
import yaml

dpn = {'url': 'http://ec2-54-226-144-188.compute-1.amazonaws.com'}
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json', 'Authorization': 'Token token=dpn_token'}

# Verify record was passed on command line
# Read content from stdin
input_record=sys.stdin.read().replace('\n', '')
# log_message("length of JSON input " + str(len(input_record)))
if len(input_record) is 0:
    log_message("Record required as input")
    exit(1) 
sync_record=json.loads(input_record)
dpn_querystring="/api-v2/bag/"+sync_record['uuid']
response = requests.get(dpn['url']+dpn_querystring, headers=dpn_headers)
if response.status_code is not 200:
    log_message("Return code: " + str(response.status_code))
    exit(1)

response_record=json.loads(response.text)
# log_message("uuid: "+sync_record['uuid']+"="+response_record['uuid']+"; updated: "+sync_record['updated_at']+"="+response_record['updated_at'])

if sync_record['updated_at'] > response_record['updated_at']:
#    log_message("update sync record")
    update_response=requests.put(dpn['url']+dpn_querystring, headers=dpn_headers, data=input_record)
    if update_response.status_code is not 200:
        log_message("Return code: " + str(update_response.status_code))
	exit(1)
else:
    if response_record['updated_at'] > sync_record['updated_at']:
        log_message("local record is newer")
    else:
        log_message("records match")
exit(0)

