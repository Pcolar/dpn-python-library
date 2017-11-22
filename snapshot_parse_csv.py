""" Parse snapshot report """

from app.dpn_python_library import *
import requests
import datetime
import sys
import os

def reset_headers(headers):
    headers['snapshot']=""
    headers['bag']=""
    headers['repl']=""
    headers['node']=""
    headers['requested']=""
    headers['stored']=""
    headers['cancelled']=""
    return

def print_record(headers):
    print headers['snapshot']+","+headers['bag']+","+headers['repl']+","+headers['node']+","+headers['requested']+","+headers['stored']+","+headers['cancelled']
    return

def t_or_f(tf_string):
    if (tf_string.endswith("true")):
       return "T"
    else:
       return "F"

started=end=0
headers={}
reset_headers(headers)
print "Snapshot,Bag,Replication ID,Node,Requested,Stored,Cancelled"
while (started == 0):
    # Read record from stdin until "start"
    input_record=sys.stdin.readline()
#    log_message(input_record)
    if input_record.startswith("start"):
        started = 1

while (end == 0):
    input_record=sys.stdin.readline()
#    log_message(input_record)
    if input_record.startswith("end "):
        end = 1
        continue
    if input_record.startswith("===="):
        reset_headers(headers)
        continue
    if (headers['snapshot'] is ""):
        headers['snapshot'] = input_record.rstrip()
        continue
    if input_record.startswith("Bag"):
        string_list = input_record.split()
        headers['bag'] = string_list[1]
        continue
    # replication records
    string_list = input_record.split()
    headers['repl'] = string_list[0]
    headers['node'] = string_list[1]
    if (string_list[2].startswith("store_requested")):
        headers['requested']=t_or_f(string_list[2])
    if (string_list[3].startswith("stored")):
        headers['stored']=t_or_f(string_list[3])
    if (string_list[4].startswith("cancelled")):
        headers['cancelled']=t_or_f(string_list[4])
    print_record(headers)
