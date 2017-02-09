"""DPN Python Library"""
import json
import csv
import datetime
import boto3

# constants
#True = 1
#False = 0

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
                    log_message("SQS entry was not a DCV Filename notification: " \
                        + json_records['Records'][0]['s3']['configurationId'])
                    continue
            if filename:
                # Let the queue know that the message is processed
                log_message("Deleting message: " + json_message['MessageId'])
                message.delete()
                return filename
            else:
                # leave the entry in the queue
                return

def  create_csv(json_file):
    """create a csv file from the json data"""
    output_filename = json_file[:json_file.find('json')] + "csv"
    log_message(output_filename)
    output_file = open(output_filename, 'w')
    csvwriter = csv.writer(output_file)
    first_row = True
    with open(json_file) as input_file:
        json_data = json.load(input_file)
        for keys in json_data.keys():
            records = json_data[keys]
    rec_num = 0
    while rec_num < len(records):
        record = records[rec_num]
        if first_row:
            csvwriter.writerow(record.keys())
            first_row = False
        values = record.values()
        values = [char.encode(encoding='ascii', errors='replace') for char in values]
        csvwriter.writerow(values)
        rec_num += 1
    log_message(len(records))
    input_file.close()
    output_file.close()


json_file = snapshot_file()
if json_file:
    create_csv(json_file)

