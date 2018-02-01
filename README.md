# dpn-python-library
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fc2c86b867c54f7a927fe251bd61b4bc)](https://www.codacy.com/app/dave_9/dpn-python-library?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Pcolar/dpn-python-library&amp;utm_campaign=Badge_Grade)

## Python code for DPN client functions

### NiFi 
This directory contains template files extracted from production NiFi instances

### app
Contains python libraries

### Utilities

#### BagCreateUpdate.py
Encapsulates DPN API GET and POST calls to update a registry bag record via the DPN API

#### audit_bag_repl.py, audit_repl.py
Validates number  of replications meets policy

#### create-dict.py
Creates a dictionary from file input

#### create-digest.py
Creates a digest record, via the API, from file input

#### create_dpn_bag.py, create_dpn_bag_stdin.py, create_update_bag.py
Creates (or updates) a bag entry via the DPN API

#### create-fixity.py
Creates a fixity record, via the API, from file input

#### create-ingest.py
Creates an ingest record, via the API, from file input

#### create_update_member.py
Creates (or updates) a member record via the DPN API

#### create_update_repl.py
Creates (or updates) a replication record via the DPN API

#### get_api_endpoint.py
DPN API call shell

#### snapshot_parse_csv.py
Parse the UCSD DCV 'conan' report into CSV

#### update_bag_repl_nodes.py
Given a satisfied Repl record at STDIN, Update the corresponding bag record
