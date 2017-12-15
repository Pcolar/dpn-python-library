#!/usr/bin/python
""" Execution shell for DPN API get calls """

from dpn_python_library import *
import json
import requests
import sys
import os

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

# Read content from stdin
try:
    input_record=sys.stdin.read().replace('\n', '')
    # log_message("length of JSON input " + str(len(input_record)))
    if len(input_record) is 0:
        log_message("Record required as input")
        exit(1)
    sync_record=json.loads(input_record)

except:
    log_message("JSON formatted record required as input")
    exit(1)

dpn_querystring="/api-v2/bag/"+sync_record['uuid']
response = requests.get(dpn_host+dpn_querystring, headers=dpn_headers)
if response.status_code is 200:
    response_record=json.loads(response.text)
#    log_message("uuid: "+sync_record['uuid']+"="+response_record['uuid']+"; updated: "+sync_record['updated_at']+"="+response_record['updated_at'])

    if sync_record['updated_at'] > response_record['updated_at']:
        log_message("update sync record")
        update_response=requests.put(dpn_host+dpn_querystring, headers=dpn_headers, data=input_record)
        if update_response.status_code is not 200:
            log_message("Return code: " + str(update_response.status_code))
            exit(1)
#    else:
#        if response_record['updated_at'] > sync_record['updated_at']:
#            log_message("local record is newer")
#        else:
#            log_message("records match")
else:
    log_message("Status: " + str(response.status_code)+ "; uuid: " + sync_record['uuid'])
#    if response.status_code is 404:
    log_message("Creating record")
    update_response=requests.post(dpn_host+"/api-v2/bag", headers=dpn_headers, data=input_record)
    if update_response.status_code is not 201:
            log_message("Create failed: " + str(update_response.status_code))
            exit(1)
exit(0)
