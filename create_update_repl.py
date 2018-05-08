#!/usr/bin/python
""" Synchronize DPN Replication Records """

from app.dpn_python_library import *
import json
import requests
import sys

# Retrieve environment variables
dpn_host, dpn_token = load_environment()
token_string="Token token="+dpn_token
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json', 'Authorization': token_string}
#log_message("DPN Host: "+dpn_host+" DPN Token: "+dpn_token)
#log_message("DPN Headers: "+json.dumps(dpn_headers))
json_messages={}

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
    create_response=requests.post(dpn_host+dpn_api_endpoint, headers=dpn_headers, data=input_record)
    if create_response.status_code is not 201:
        json_messages['message'] = "Create Repl record Failed"
        json_messages['repl_uuid'] = sync_record['replication_id']
        json_messages['return_code'] = str(create_response.status_code)
        log_json_message(json_messages)
        exit(1)
    else:
        json_messages['message'] = "Created Repl record"
        json_messages['repl_uuid'] = sync_record['replication_id']
        json_messages['return_code'] = str(create_response.status_code)
        log_json_message(json_messages)

else:
    if target_response.status_code == 200:
        #successful retrieval
        target_record=json.loads(target_response.text)
        if sync_record['updated_at'] > target_record['updated_at']:
            update_response=requests.put(dpn_host+dpn_querystring, headers=dpn_headers, data=input_record)
            if update_response.status_code is not 200:
		error_response=json.loads(update_response.text)
                json_messages['message'] = "Update Repl record Failed"
                json_messages['repl_uuid'] = sync_record['replication_id']
                json_messages['return_code'] = str(update_response.status_code)
                json_messages['errors'] = error_response['errors']
                log_json_message(json_messages)
                exit(1)
	    else:
                json_messages['message'] = "Updated Repl record"
                json_messages['repl_uuid'] = sync_record['replication_id']
                json_messages['return_code'] = str(update_response.status_code)
                log_json_message(json_messages)
    else:
	# log_message("Retrieval failed " + str(target_response.status_code)+" repl: "+sync_record['replication_id'])
        json_messages['message'] = "Retrieve Repl record Failed"
        json_messages['repl_uuid'] = sync_record['replication_id']
        json_messages['return_code'] = str(target_response.status_code)
        log_json_message(json_messages)
exit(0)
