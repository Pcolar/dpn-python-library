#!/usr/bin/python
""" Retrieves a json file from an S3 bucket and converts to csv"""

from app.dpn_python_library import *
import sys

# Read content from stdin
json_file=sys.stdin.read().replace('\n', '')

# if it exists, download the file and convert to CSV
if len(json_file) > 0:
    download_s3_file(json_file)
    create_csv(json_file)
#    delete_s3_file(json_file)
else:
    log_message("File name required as input")
    exit(1)
exit(0)
