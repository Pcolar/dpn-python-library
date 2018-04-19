#!/bin/bash
set +v
export filedate=$1

export queue="DPN-Replication-Sync"
export infile="/dpn/replications_$filedate.json"
~/dpn-python-library/copy_file_to_SQS.py 

export queue="DPN-BagRecord-Sync"
export infile="/dpn/bags_$filedate.json"
~/dpn-python-library/copy_file_to_SQS.py

export queue="DPN-NiFi-DIgest-Sync"
export infile="/dpn/digest_$filedate.json"
~/dpn-python-library/copy_file_to_SQS.py

export infile="/dpn/fixity_$filedate.json"
export queue="DPN-NiFi-Fixity-Sync"
~/dpn-python-library/copy_file_to_SQS.py

export queue="DPN-NiFi-Ingest-Sync"
export infile="/dpn/ingest_$filedate.json"
~/dpn-python-library/copy_file_to_SQS.py
