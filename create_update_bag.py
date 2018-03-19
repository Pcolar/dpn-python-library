#!/usr/bin/python
""" Given a json bag record, create or update in the target system """

from app.dpn_python_library import *
import json
import requests
import sys

json_messages={}
# Retrieve environment variables
dpn_host, dpn_token = load_environment()
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json'}
dpn_headers['Authorization']="Token token="+dpn_token
#log_message("DPN Host: "+dpn_host)
#log_message("DPN Headers: "+json.dumps(dpn_headers))

# Read content from stdin
try:
    input_record=sys.stdin.read().replace('\n', '')
    # log_message("length of JSON input " + str(len(input_record)))
    if len(input_record) == 0:
        log_message('"message": "Bag Record required as input"')
        exit(1)
    sync_record=json.loads(input_record)

except (ValueError, IndexError):
    log_message('"message": "JSON formatted Bag record required as input"')
    exit(1)

dpn_querystring="/api-v2/bag/"+sync_record['uuid']
response = requests.get(dpn_host+dpn_querystring, headers=dpn_headers)
if response.status_code is 200:
    response_record=json.loads(response.text)
#    log_message("uuid: "+sync_record['uuid']+"="+response_record['uuid']+"; updated: "+sync_record['updated_at']+"="+response_record['updated_at'])

    if sync_record['updated_at'] > response_record['updated_at']:
        json_messages['message'] = "updating bag record"
	json_messages['bag_uuid'] = sync_record['uuid']
	log_json_message(json_messages)
        update_response=requests.put(dpn_host+dpn_querystring, headers=dpn_headers, data=input_record)
        if update_response.status_code is not 200:
	    json_messages['message'] = "Update Bag Failed"
            json_messages['return_code'] = str(update_response.status_code)
            json_messages['bag_uuid'] = sync_record['uuid']
            log_json_message(json_messages)
            exit(1)
#    else:
#        if response_record['updated_at'] > sync_record['updated_at']:
#            log_message("local record is newer")
#        else:
#            log_message("records match")
else:
    json_messages['message'] = "creating bag record"
    json_messages['bag_uuid'] = sync_record['uuid']
    json_messages['return_code'] = str(response.status_code)
    log_json_message(json_messages)
#    if response.status_code is 404:
    update_response=requests.post(dpn_host+"/api-v2/bag", headers=dpn_headers, data=input_record)
    if update_response.status_code is not 201:
	    json_messages['message'] = "create bag failed"
	    json_messages['bag_uuid'] = sync_record['uuid']
	    json_messages['return_code'] = str(update_response.status_code)
	    log_json_message(json_messages)
            exit(1)
exit(0)
