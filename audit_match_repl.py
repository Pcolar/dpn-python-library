#!/usr/bin/python
""" Validate records match between nodes """
#A replication may have the following states:
#
#"store_requested"   "stored"    "cancelled"   Description
# False               False        False       Initial state - request created by from_node, but not serviced
# True/False          True/False   True        Transaction Cancelled, by from_node or to_node
# False               False        False       Checksum updated by to_node after successful retrieval, waiting on from_node acknowledgement
# True                False        False       Request Acknowledged by from_node
# True                False        True        Request Denied - a reason must be added in "cancel_reason","cancel_reason_detail"
# True                True         False       Bag retrieved, validated and stored in local environment

from app.dpn_python_library import *
import json
import requests
import sys

# Retrieve environment variables
dpn_host, dpn_token = load_environment()
# log_message("DPN Host: "+dpn_host+" DPN Token: "+dpn_token)
# log_message("DPN Headers: "+json.dumps(dpn_headers))
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json'}
dpn_headers['Authorization']="Token token="+dpn_token

out_record={}
record_flag=False

# Read content from stdin
input_record=sys.stdin.read().replace('\n', '')

# log_message("length of JSON input " + str(len(input_record)))
if len(input_record) is 0:
    log_message("Record required as input")
    exit(1)

repl_record=json.loads(input_record)
#print json.dumps(repl_record)

## Retrieve Repl record from other node
# Querystring to drive retrieval from Target
dpn_api_endpoint="/api-v2/replicate/"
dpn_querystring=dpn_api_endpoint+repl_record['replication_id']
#log_message("retrieving " + dpn_querystring)

# retrieve the Target record for comparison
target_response = requests.get(dpn_host+dpn_querystring, headers=dpn_headers)
#log_message("retrieval status: "+str(target_response.status_code))

if target_response.status_code != 200:
    # Target record does not exist
    out_record['retrieval_error']="Record " + str(repl_record['replication_id']) + " not retrieved from "+ dpn_host
    out_record['status_code']=target_response.status_code
    log_json_message(out_record)
    exit(0)
else:
    target_record=json.loads(target_response.text)
    if  repl_record['cancelled'] != target_record['cancelled'] or repl_record['store_requested'] != target_record['store_requested'] or \
    repl_record['stored'] != target_record['stored'] or repl_record['fixity_value'] != target_record['fixity_value']:
        out_record['reason']="No Match"
        record_flag=True

if record_flag is True:
    out_record['replication_id']=repl_record['replication_id']
    out_record['source_store_requested']=repl_record['store_requested']
    out_record['target_store_requested']=target_record['store_requested']
    out_record['source_fixity']=repl_record['fixity_value']
    out_record['target_fixity']=target_record['fixity_value']
    out_record['source_stored']=repl_record['stored']
    out_record['target_stored']=target_record['stored']
    out_record['source_cancelled']=repl_record['cancelled']
    out_record['target_cancelled']=target_record['cancelled']
    out_record['from_node']=repl_record['from_node']
    out_record['to_node']=repl_record['to_node']
    out_record['source_updated_at']=repl_record['updated_at']
    out_record['target_updated_at']=target_record['updated_at']
    log_json_message(out_record)
exit(0)
