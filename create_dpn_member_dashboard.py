#!/usr/bin/python

from app.dpn_python_library import *
import requests
import sys

## Create the member deposit dashboards

# Retrieve environment variables
dpn_host, dpn_token = load_environment()
dpn_headers={'Content-Type': 'application/json','Accept': 'application/json'}
dpn_headers['Authorization']="Token token="+dpn_token
log_message("DPN Host: "+dpn_host)
log_message("DPN Headers: "+json.dumps(dpn_headers))
endpoint = {'bag': '/api-v2/bag', 'member': '/api-v2/member', 'node': '/api-v2/node', 'repl': '/api-v2/replicate'}

# Retrieve the file
json_file = "Members.json"
s3_bucket =  "dpn-config"
download_s3_file(json_file, s3_bucket)

# Retrieve the file
json_file = "Members.json"
s3_bucket =  "dpn-config"
download_s3_file(json_file, s3_bucket)

# Read content from file
#    output_filename = json_file[:json_file.find('json')] + "csv"
#    log_message("File created: " + output_filename)
#    output_file = open(output_filename, 'w')
#    csvwriter = csv.writer(output_file)

try:
    with open(json_file) as input_file:
        json_data = json.load(input_file)
        for keys in json_data.keys():
            members = json_data[keys]
#      rec_num = 0
#      while rec_num < len(members):
#          record = records[rec_num]
#          if first_row:
#              csvwriter.writerow(record.keys())
#              first_row = False
#          values = record.values()
        # csvwriter is ascii only - change encoding
#          values = [char.encode(encoding='ascii', errors='replace') for char in values]
#          csvwriter.writerow(values)
#          rec_num += 1
except ClientError as boto3_error:
    log_message("ERROR: File " + json_file + " not found")
    log_message(boto3_error.message)
else:
    log_message("Rows exported: " + str(len(records)))
    input_file.close()

    output_file.close()

dpn_bag=sys.stdin.read().replace('\n', '')
# log_message("length of JSON input " + str(len(dpn_bag)))
if len(dpn_bag) == 0:
    log_message("Bag record required as input")
    exit(1)

#log_message(dpn_headers)
#log_message(dpn_bag)

response = requests.post(dpn_host+endpoint['bag'], headers=dpn_headers, data=dpn_bag)
log_message("Return code: " + str(response.status_code))
log_message(response.text)

if  response.status_code is 201:
    exit(0)
exit(1)
