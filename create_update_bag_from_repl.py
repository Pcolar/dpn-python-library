#!/usr/bin/python
""" Given a satisfied Repl record at STDIN, Create a corresponding bag record and write to STDOUT """

from app.dpn_python_library import *
import json
import requests
import sys


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
    if len(input_record) is 0:
        log_message("Record required as input")
        exit(1)
    repl_record=json.loads(input_record)
except (ValueError, IndexError):
    log_message("JSON record required as input")
    exit(1)

# Completed Replications have store_requested, stored, and a checksum
if repl_record['store_requested'] is not True or repl_record['stored'] is not True or repl_record['fixity_value'] is "":
#   replication not completed
#   log_message("Replication record: "+ repl_record['replication_id'] + " not complete")
    exit(0)

dpn_querystring="/api-v2/bag/"+repl_record['bag']
response = requests.get(dpn_host+dpn_querystring, headers=dpn_headers)
if response.status_code is 200:
    bag_record=json.loads(response.text)
#   print json.dumps(bag_record)
#   Is the to_node in the replication list?
    if repl_record['to_node'] not in bag_record['replicating_nodes']:
        bag_record['replicating_nodes'].append(repl_record['to_node'])
        out_record=json.dumps(bag_record)
#        print json.dumps(out_record)
#        log_message("bag record Updated "+ repl_record['bag'])
#        update_response=requests.put(dpn_host+dpn_querystring, headers=dpn_headers, data=out_record)
#        if update_response.status_code is not 200:
#            log_message("Return code: " + str(update_response.status_code))
#            exit(1)
        print out_record
else:
#    log_message("Bag not retrieved: " + str(response.status_code)+ " Bag: "+ str(repl_record['bag']))
    exit(1)
exit(0)
