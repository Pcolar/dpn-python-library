"""DPN Python Library"""
__copyright__ = "Copyright (C) 2017 Digital Preservation Network, LLC"
__license__ = "BSD Version 3 License"


import json
import csv
import datetime
import time
import os
import boto3
from botocore.exceptions import ClientError
import requests

# constants
#True = 1
#False = 0

# Note: create the credentials file in .aws before using
#
def dpn_time():
    return time.strftime('%Y-%m-%dT%H:%M:%S.000Z')

def log_message(message):
    """print out  in log message format"""
    print "%s:  %s" % (datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), message)

def log_json_message(log_message):
    """print out  in json tagged log message format"""
    log_message['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    print json.dumps(log_message)
    log_message={}

def  create_csv(json_file):
    """create a csv file from the json data"""
    output_filename = json_file[:json_file.find('json')] + "csv"
    log_message("File created: " + output_filename)
    output_file = open(output_filename, 'w')
    csvwriter = csv.writer(output_file)
    first_row = True
    try:
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
        # csvwriter is ascii only - change encoding
          values = [char.encode(encoding='ascii', errors='replace') for char in values]
          csvwriter.writerow(values)
          rec_num += 1
    except ClientError as boto3_error:
      log_message("ERROR: File " + json_file + " not found")
      log_message(boto3_error.message)
    else:
      log_message("Rows exported: " + str(len(records)))
      input_file.close()

    output_file.close()

def download_s3_file(json_file, s3_bucket='dpn-dcv'):
    """ dowload an object from a s3 bucket """
    if json_file:
        # connect to the S3 service
        s3 = boto3.resource('s3')
        # download the object
        try:
          s3.Object(s3_bucket, json_file).download_file(json_file)
        except ClientError as boto3_error:
          log_message("ERROR: S3 object not found " + json_file)
          log_message(boto3_error.message)

def delete_s3_file(file_object, s3_bucket='dpn-dcv'):
    """  Delete a file object from S3 """
    if file_object:
	# connect to the S3 service and
        # delete the object
        client = boto3.client('s3')
        client.delete_object(Bucket=s3_bucket, Key=file_object)
        log_message("Object Deleted: " + file_object)

def get_uuidv4():
    """ Call service for UUID v4  """
    response = requests.get('https://www.uuidgenerator.net/api/version4')
    if response.status_code is 200:
      uuid=r.text
      log_message("UUID: " + uuid)
    return uuid

def load_environment():
# read content from environment variables
# expecting Host, Token
#
    if  "dpn_host" in os.environ:
        dpn_host = os.environ['dpn_host']
    else:
        log_message("Expecting: dpn_host, dpn_token")
        exit(1)
    if  "dpn_token" in os.environ:
        dpn_token = os.environ['dpn_token']
    else:
        log_message("Expecting: dpn_host, dpn_token")
        exit(1)
    return dpn_host, dpn_token
