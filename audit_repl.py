#!/usr/bin/python
""" Validate # of replications meets policy """
#A replication may have the following states:
#
#"store_requested"   "stored"    "cancelled"   Description
# False               False        False       Initial state - request created but not serviced
# False               False        True        Transaction Cancelled
# True                False        False       Request Acknowledged
# True                False        True        Request Denied - a reason must be added in "cancel_reason","cancel_reason_detail"
# True                True         False       Bag retrieved, validated and stored in local environment
#                                               A checksum must be added to complete the transaction

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

if  repl_record['cancelled'] is True and repl_record['cancel_reason'] == "":
    out_record['reason']="Replication cancelled without reason"
    record_flag=True
    #print out_record['reason']

if  repl_record['store_requested'] is True and repl_record['stored'] is True and repl_record['fixity_value'] == "":
    out_record['reason']="Replication stored but not checksummed"
    record_flag=True
    #print out_record['reason']

if  repl_record['store_requested'] is False and repl_record['stored'] is False and repl_record['cancelled'] is False:
    out_record['reason']="Replication unprocessed"
    record_flag=True

if record_flag is True:
    out_record['replication_id']=repl_record['replication_id']
    out_record['store_requested']=repl_record['store_requested']
    out_record['stored']=repl_record['stored']
    out_record['cancelled']=repl_record['cancelled']
    out_record['from_node']=repl_record['from_node']
    out_record['to_node']=repl_record['to_node']
    out_record['updated_at']=repl_record['updated_at']
    print json.dumps(out_record)
exit(0)
