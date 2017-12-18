#!/usr/bin/python
""" Synchronize DPN Replication Records """

from dpn_python_library import *
import json
import requests
import sys
import os

# read content from environment variables
# expecting Host
#
try:
    dpn_host = os.environ['dpn_host']
#    log_message("Host: "+os.environ['dpn_host'])
except (ValueError, IndexError):
    log_message("expected dpn_host environment variable")
    exit(1)

#log_message("DPN Host: "+dpn_host)
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json', 'Authorization': 'Token token=dpn_token'}

# Read synchronization record from stdin
input_record=sys.stdin.read().replace('\n', '')
if len(input_record) == 0:
    log_message("Record required as input")
    exit(1)
sync_record=json.loads(input_record)

# Querystring to drive retrieval from Target
dpn_api_endpoint="/api-v2/replicate/"
dpn_querystring=dpn_api_endpoint+sync_record['replication_id']
#log_message("retrieving " + dpn_querystring)

# retrieve the Target record for comparison, update, or creation
target_response = requests.get(dpn_host+dpn_querystring, headers=dpn_headers)
#log_message("retrieval status: "+str(target_response.status_code))

if target_response.status_code == 404:
    # Target record does not exist
    log_message("Creating record "+sync_record['replication_id'])
    create_response=requests.post(dpn_host+dpn_api_endpoint, headers=dpn_headers, data=input_record)
    if create_response.status_code != 201:
        log_message("Create failed " + str(create_response.status_code))
        exit(1)
else:
    if target_response.status_code == 200:
        #successful retrieval
        target_record=json.loads(target_response.text)
        if sync_record['updated_at'] > target_record['updated_at']:
            log_message("updating repl record "+sync_record['replication_id'])
            update_response=requests.put(dpn_host+dpn_querystring, headers=dpn_headers, data=input_record)
            if update_response.status_code != 200:
                log_message("Update failed " + str(update_response.status_code))
                exit(1)
exit(0)

