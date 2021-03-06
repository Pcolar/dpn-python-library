#!/usr/bin/python
""" Synchronize DPN Ingest Records """

from app.dpn_python_library import *
import json
import requests
import sys

# get access info from the environment
dpn_host, dpn_token = load_environment()
# log_message("DPN Host: "+dpn_host+" DPN Token: "+dpn_token)

token_string="Token token="+dpn_token
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json', 'Authorization': token_string}

# Read synchronization record from stdin
input_record=sys.stdin.read().replace('\n', '')
if len(input_record) == 0:
    log_message("Record required as input")
    exit(1)
sync_record=json.loads(input_record)

# Querystring to drive retrieval from Target
dpn_api_endpoint="/api-v2/ingest"
dpn_querystring=dpn_api_endpoint
# log_message("Querystring " + dpn_querystring)

# Fixity records are immutable once created
# We use a post to attempt creation, if it fails
#  409 - Duplicate - OK
#  201 - Created
#  xxx - fail

create_response=requests.post(dpn_host+dpn_querystring, headers=dpn_headers, data=input_record)
if create_response.status_code == 201:
    log_message("Created Ingest record for bag: "+sync_record['bag'])
else:
    if create_response.status_code == 409:
#     	log_message("Duplicate Ingest record " + str(create_response.status_code)+" Bag UUID: "+ str(sync_record['bag']))
	pass
    else:
        log_message("Ingest record create failed " + str(sync_record['ingest_id']) + " Status: " + str(create_response.status_code))
exit(0)
