#!/usr/bin/env bash
## dpn-sync.sh
## Script for syncing DPN records on a weekly basis to an s3 bucket
## Dependencies: awscli (pip install awscli --upgrade --user && aws configure)


# Check for environment variables
if [[ -z ${API_TOKEN} ]];
then
    echo "API_TOKEN required"
    exit -1
fi

if [[ -z ${REST_SERVER} ]];
then
    echo "REST_SERVER required"
    exit -1
fi

if [[ -z ${DEST_DIRECTORY} ]];
then
    echo "DEST_DIRECTORY not found, reverting to dpn"
    DEST_DIRECTORY="dpn"
fi

# set up environment

JSON_DIR="/tmp/dpn/${DEST_DIRECTORY}"
# S3_BUCKET="dpn-sync"
# API_TOKEN="<insert token here>"

DATE_AFTER=$(date --iso-8601 -d "-1 week")
DATE_BEFORE=$(date --iso-8601)
DATE_PARAMS="after=${DATE_AFTER}&before=${DATE_BEFORE}"
PAGE_PARAMS="page=1&page_size=1"

BAG_API="https://${REST_SERVER}/api-v2/bag?admin_node=chron&${DATE_PARAMS}"
DIGEST_API="https://${REST_SERVER}/api-v2/digest?${DATE_PARAMS}"
INGEST_API="https://${REST_SERVER}/api-v2/ingest?${DATE_PARAMS}"
FIXITY_API="https://${REST_SERVER}/api-v2/fixity_check?node=chron&${DATE_PARAMS}"
REPLICATION_API="https://${REST_SERVER}/api-v2/replicate?from_node=chron&${DATE_PARAMS}"

get_json() {
  URL="${1}&${PAGE_PARAMS}"
  echo "GETing ${URL}"
  PAGE_SIZE=$(curl --insecure -s -H "Authorization: Token token=${API_TOKEN}" "${URL}" | sed -r 's/^\{\"count\":([0-9]+).*/\1/')
  if [ ${PAGE_SIZE} -eq 0 ]; then
      PAGE_SIZE="1"
  fi

  PARAMS="page=1&page_size=${PAGE_SIZE}"
  URL="${1}&${PARAMS}"
  echo "------------------------"
  echo "${PAGE_SIZE} records found"
  if [ ${PAGE_SIZE} -gt 100 ]
  then
      echo "${PAGE_SIZE}  is greater than 100, defaulting to 100 records"
      PAGE_SIZE="100"
  fi
  echo "Writing ${URL} to ${2}"
  echo "------------------------"
  curl --insecure -s -H "Authorization: Token token=${API_TOKEN}" "${URL}" -o ${2}
}

mkdir -p ${JSON_DIR}
get_json $BAG_API "${JSON_DIR}/bags_${DATE_BEFORE}.json"
get_json $DIGEST_API "${JSON_DIR}/digest_${DATE_BEFORE}.json"
get_json $INGEST_API "${JSON_DIR}/ingest_${DATE_BEFORE}.json"
get_json $FIXITY_API "${JSON_DIR}/fixity_checks_${DATE_BEFORE}.json"
get_json $REPLICATION_API "${JSON_DIR}/replications_${DATE_BEFORE}.json"

# aws s3 cp --recursive ${JSON_DIR} "s3://${S3_BUCKET}/${DEST_DIRECTORY}"
