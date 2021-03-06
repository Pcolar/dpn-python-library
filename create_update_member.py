
#!/usr/bin/python
""" Synchronize DPN Member Records """

from app.dpn_python_library import *
import json
import requests
import sys


# Retrieve environment variables
dpn_host, dpn_token = load_environment()
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json'}
dpn_headers['Authorization']="Token token="+dpn_token
# log_message("DPN Host: "+dpn_host+" DPN Token: "+dpn_token)
# log_message("DPN Headers: "+json.dumps(dpn_headers))

# Read synchronization record from stdin
input_record=sys.stdin.read().replace('\n', '')
if len(input_record) == 0:
    log_message("Record required as input")
    exit(1)
sync_record=json.loads(input_record)

# Querystring to drive retrieval from Target
dpn_api_endpoint="/api-v2/member/"
dpn_querystring=dpn_api_endpoint+sync_record['member_id']
#log_message("retrieving " + dpn_querystring)

# retrieve the Target record for comparison, update, or creation
target_response = requests.get(dpn_host+dpn_querystring, headers=dpn_headers)
#log_message("retrieval status: "+str(target_response.status_code))

if target_response.status_code == 404:
    # Target record does not exist
    log_message("Creating record "+sync_record['member_id'])
    create_response=requests.post(dpn_host+dpn_api_endpoint, headers=dpn_headers, data=input_record)
    if create_response.status_code is not 201:
        log_message("Create failed " + str(create_response.status_code))
        exit(1)
else:
    if target_response.status_code == 200:
        #successful retrieval
        target_record=json.loads(target_response.text)
        if sync_record['updated_at'] > target_record['updated_at']:
            log_message("updating member record "+sync_record['member_id'])
            update_response=requests.put(dpn_host+dpn_querystring, headers=dpn_headers, data=input_record)
            if update_response.status_code is not 200:
                log_message("Update failed " + str(update_response.status_code))
                exit(1)
    else:
        log_message("Retrieval failed " + str(target_response.status_code)+" repl: "+sync_record['member_id'])
exit(0)

