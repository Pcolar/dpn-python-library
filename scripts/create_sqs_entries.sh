#! /bin/bash
#  Create SQS query strings for DPN Synchronization
# set -x

echo "Bags"
export queue="DPN-NiFi-Flow"
export query_string="/api-v2/bag?after="`date --date='00:00 2 weeks ago' +'%Y-%m-%dT%H:%M:%S.000Z'`"&page_size=1"
echo $query_string | ~/dpn-python-library/create_sqs_from_stdin.py

echo ""
echo "Digest"
export queue="DPN-NiFi-DIgest-Flow"
export query_string="/api-v2/digest?after="`date --date='00:00 2 weeks ago' +'%Y-%m-%dT%H:%M:%S.000Z'`"&page_size=1"
echo $query_string | ~/dpn-python-library/create_sqs_from_stdin.py

echo ""
echo "Fixity"
export queue="DPN-NiFi-Fixity-Flow"
export query_string="/api-v2/fixity_check?after="`date --date='00:00 2 weeks ago' +'%Y-%m-%dT%H:%M:%S.000Z'`"&page_size=1"
echo $query_string | ~/dpn-python-library/create_sqs_from_stdin.py

echo ""
echo "Ingest"
export queue="DPN-NiFi-Ingest-Flow"
export query_string="/api-v2/ingest?after="`date --date='00:00 2 weeks ago' +'%Y-%m-%dT%H:%M:%S.000Z'`"&page_size=1"
echo $query_string | ~/dpn-python-library/create_sqs_from_stdin.py

echo ""
echo "Replication"
export queue="DPN-NiFi-Repl-Flow"
export query_string="/api-v2/replicate?after="`date --date='00:00 2 weeks ago' +'%Y-%m-%dT%H:%M:%S.000Z'`"&page_size=1"
echo $query_string | ~/dpn-python-library/create_sqs_from_stdin.py
