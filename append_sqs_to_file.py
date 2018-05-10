#!/usr/bin/python
""" Append the contents of an SQS queue to a file """
# note: assumes credential file is present in home directory path

from app.dpn_python_library import *

def load_environment_variables():
# read content from environment variables
# expecting  queue, filename
#
    if  "queue" in os.environ:
        queue_name = os.environ['queue']
    else:
        log_message("Expecting: queue, outfile")
        exit(1)
    if  "outfile" in os.environ:
        output_file = os.environ['outfile']
    else:
        log_message("Expecting: queue, outfile")
        exit(1)
    if  "delete_sqs" in os.environ:
        delete_sqs = true
    else:
        delete_sqs = false
    if  "json_out" in os.environ:
        json_out = true
    else:
        json_out = false
    return  queue_name, output_file, delete_sqs, json_out

true=1
false=0
message_count=0
queue_name, output_file, delete_sqs, json_out = load_environment_variables()

if queue_name == ""  or output_file == "":
    log_message("expecting queue name and out filename")
    exit(1)

# Get the service resource
sqs = boto3.resource('sqs')
# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName=queue_name)

# Open the output file in write mode
file_handle = open(output_file, "a+")
if json_out is true:
    file_handle.write("{ \"results\": [\n")
# Read and process the queue entries
message_received = true
while message_received is true:
    messages = queue.receive_messages(WaitTimeSeconds=20, MaxNumberOfMessages=1)
    if len(messages) > 0:
        for message in messages:
            if json_out is true:
                file_handle.write(message.body+',\n')
            else:
                file_handle.write(message.body+'\n')
	    message_count +=1
            if delete_sqs is true:
                message.delete()
    else:
	message_received = false

if json_out is true:
    file_handle.write("] }")
log_messages={'records': message_count, 'queue': queue_name}
log_json_message(log_messages)
file_handle.close()
exit(0)
