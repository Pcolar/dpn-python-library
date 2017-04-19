## create dictionaries of DPN v2 data structures

bag_keys = ["uuid","ingest_node","replicating_nodes","admin_node","member","local_id","size","first_version_uuid","version","bag_type","created_at","updated_at"]
bag = {}
digest_keys = ["bag","algorithm","node","value","created_at"]
digest = {}
fixity_keys = ["fixity_check_id","bag","node","success","fixity_at","created_at"]
fixity = {}
ingest_keys = ["ingest_id","bag","ingested","replicating_nodes","created_at"]
ingest = {}
member_keys = ["member_id","name","email"]
member = {}
node_keys = ["name","namespace","api_root","ssh_pubkey","protocols","storage/region","storage/type","replicate_from","replicate_to","restore_from","restore_to","fixity_algorithms","created_at","updated_at"]
node = {}
restore_keys = ["bag","created_at","updated_at","restore_id","from_node","to_node","protocol","link","accepted","finished","cancelled","cancel_reason"]
restore = {}
replication_keys = ["from_node","to_node","bag","replication_id","fixity_algorithm","fixity_nonce","fixity_value","protocol","link","stored","store_requested","cancelled","cancel_reason","created_at","updated_at"]
replication = {}

def list_to_dict(listname, dictname):
    # create the dictionary with keys and null values
    for key in listname:
      dictname[key] = ''

##  USAGE: list_to_dict(bag_keys, bag)


