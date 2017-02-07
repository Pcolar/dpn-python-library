"""DPN Python Library"""
import json
import datetime
import boto3

# Note: create the credentials file in .aws before using
#
def log_message(message):
    """print out  in log message format"""
    print "%s:  %s" % (datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), message)

def snapshot_file():
    """Read the queue and retrieve the snapshot filename"""
    # Get the service resource
    sqs = boto3.resource('sqs')
    queue_name = 'DPN_msg'
    # Get the queue. This returns an SQS.Queue instance
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    filename = 'None'
    # Process messages
    while 1:
        messages = queue.receive_messages(WaitTimeSeconds=20, MaxNumberOfMessages=1)
        for message in messages:
            json_message = json.loads(message.body)
            if json_message['Message']:
                json_records = json.loads(json_message['Message'])
                if json_records['Records'][0]['s3']['configurationId'] == u'DCV dump Notification':
                    filename = json_records['Records'][0]['s3']['object']['key']
                else:
                    log_message("SQS entry was not a DCV Filename notification: " + json_records['Records'][0]['s3']['configurationId'])
                    continue
            if filename:
                # Let the queue know that the message is processed
                log_message("Deleting message: " + json_message['MessageId'])
                message.delete()
                return filename
            else:
                # leave the entry in the queue
                return

print snapshot_file()