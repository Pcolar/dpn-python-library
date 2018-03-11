#!/usr/bin/python
""" Appendthe contents of a file to an SQS queue """
# note: assumes credential file is present in home directory path

from app.dpn_python_library import *

def load_environment_variables():
# read content from environment variables
# expecting  queue, filename
#
    if  "queue" in os.environ:
        queue_name = os.environ['queue']
    else:
        log_message("Expecting: queue, infile")
        exit(1)
    if  "infile" in os.environ:
        input_file = os.environ['infile']
    else:
        log_message("Expecting: queue, infile")
        exit(1)
    return  queue_name, input_file


queue_name, input_file = load_environment_variables()
log_messages={}
record_count = 0
log_messages['source_file']=input_file
log_messages['queue_name']=queue_name

# Get the service resource
sqs = boto3.resource('sqs')
# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName=queue_name)

# Open the input file in read mode
file_handle = open(input_file, "r+")

# Read and process the records
for input_record in file_handle:
    # Send message to SQS queue
    response = queue.send_message(MessageBody=input_record)
    # log_json_message(response)
    record_count +=1

log_messages['record_count']=record_count
log_json_message(log_messages)
file_handle.close()
exit(0)
