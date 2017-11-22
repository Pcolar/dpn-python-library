""" Execution shell for library functions """

from app.dpn_python_library import *

# get the name of the current snapshot file via an SQS message
json_file = dcv_snapshot_file()
# if it exists, download the file and convert to CSV
if json_file:
    download_s3_file(json_file)
    create_csv(json_file)
    delete_s3_file(json_file)
