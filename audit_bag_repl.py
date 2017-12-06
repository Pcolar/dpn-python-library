#!/usr/bin/python
""" Validate # of replications meets policy """

from dpn_python_library import *
import json
import requests
import sys

dpn = {'url': 'http://ec2-54-197-14-13.compute-1.amazonaws.com'}
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json', 'Authorization': 'Token token=dpn_token'}

#  Default replication policy 
replication_copies=3
out_record={}
# Read content from stdin
input_record=sys.stdin.read().replace('\n', '')
# log_message("length of JSON input " + str(len(input_record)))
if len(input_record) is 0:
    log_message("Record required as input")
    exit(1)
sync_record=json.loads(input_record)
replication_list=sync_record['replicating_nodes']

if (len(replication_list) != replication_copies):
#    log_message("Replications records required not met " + str(sync_record['replicating_nodes']) + " UUID: " + sync_record['uuid'])
    out_record['reason']="Replications records below criteria"
    out_record['uuid']=sync_record['uuid']
    out_record['ingest_node']=sync_record['ingest_node']
    out_record['replicating_nodes']=sync_record['replicating_nodes']
    print json.dumps(out_record)
exit(0)
