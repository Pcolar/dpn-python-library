# dpn-python-library
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fc2c86b867c54f7a927fe251bd61b4bc)](https://www.codacy.com/app/dave_9/dpn-python-library?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Pcolar/dpn-python-library&amp;utm_campaign=Badge_Grade)

## Python code for DPN client functions

### API-Gateway
JSON schema files for for AWS gateway functions

### app
Contains python libraries

### scripts
Bash scripts for utility processing

### Utilities

#### append_sqs_to_file.py
Copies the contents of a queue to a local file
- if "delete_sqs" is set, the queue entries are deleted
- if "json_out" is set, a "results:" wrapper is applied for valid JSON

#### audit_bag_repl.py, audit_repl.py
Validates number  of replications meets policy

#### audit_match_repl.py
Validate replication records match between nodes

#### BagCreateUpdate.py
Encapsulates DPN API GET and POST calls to update a registry bag record via the DPN API

#### copy_file_to_SQS.py
Copies the contents of a local file to a queue

#### create-dict.py
Creates a dictionary from file input

#### create-digest.py
Creates a digest record, via the API, from file input

#### create_dpn_bag.py, create_dpn_bag_stdin.py, create_update_bag.py
Creates (or updates) a bag entry via the DPN API

#### create_dpn_member_dashboard.py
 No longer used - functionality moved to NiFi workflow engine

#### create-fixity.py
Creates a fixity record, via the API, from file input

#### create-ingest.py
Creates an ingest record, via the API, from file input

#### create_sqs_from_stdin.py
Reads a record from STDIN and creates a queue entry - single record processing only

#### create_update_bag_from_repl.py
Given a satisfied Repl record at STDIN, Create a corresponding bag record and write to STDOUT

#### create_update_member.py
Creates (or updates) a member record via the DPN API

#### create_update_repl.py
Creates (or updates) a replication record via the DPN API

#### get_api_endpoint.py
DPN API call shell

#### s3_json_to_csv.py
Retrieves a json file from an S3 bucket and converts to csv

#### snapshot_parse_csv.py
Parse the UCSD DCV 'conan' report into CSV

#### update_bag_repl_nodes.py
Given a satisfied Repl record at STDIN, Update the corresponding bag record
