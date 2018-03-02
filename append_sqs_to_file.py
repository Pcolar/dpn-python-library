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
    return  queue_name, output_file


queue_name, output_file = load_environment_variables()

# Get the service resource
sqs = boto3.resource('sqs')
# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName=queue_name)

# Open the output file in write mode
file_handle = open(output_file, "a+")

# Read and process the queue entries
message_received = 1
while message_received > 0:
    messages = queue.receive_messages(WaitTimeSeconds=20, MaxNumberOfMessages=1)
    if len(messages) > 0:
        for message in messages:
            file_handle.write(message.body+'\n')
            message.delete()

file_handle.close()
exit(0)
