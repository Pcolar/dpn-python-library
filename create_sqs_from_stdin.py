#!/usr/bin/python
""" Copy a string from STDIN to an SQS queue """

from app.dpn_python_library import *
import json
import requests
import sys

log_messages={}
def load_environment_variables():
# read content from environment variables
# expecting  queue, filename
#
    if  "queue" in os.environ:
        queue_name = os.environ['queue']
    else:
        log_message("Expecting: queue name")
        exit(1)
    return  queue_name


queue_name = load_environment_variables()
# Get the service resource
sqs = boto3.resource('sqs')
# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName=queue_name)
# Read content from stdin
try:
    input_record=sys.stdin.read().replace('\n', '')
    if len(input_record) is 0:
        log_message("Record required as input")
        exit(1)
except (ValueError, IndexError):
    log_message("Record required as input")
    exit(1)

# Send message to SQS queue
response = queue.send_message(MessageBody=input_record)

log_json_message(response)
#print(response.get('MessageId'))
#print(response.get('MD5OfMessageBody'))
exit(0)
