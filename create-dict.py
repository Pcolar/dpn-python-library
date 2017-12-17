from app.dpn_python_library import *
import csv
import json
import sys

if (len(sys.argv) is 2):
	filename = sys.argv[1]
	log_message("input filename: "+sys.argv[0])
else:
	print "Requires the input filename as a command line argument"
	exit(1)

fieldnames = ['UUID', 'NAME']
reader = csv.DictReader(open(filename, 'rU'),fieldnames=fieldnames)
members = []
for line in reader:
        print(line)
	members[line['UUID']] = line['NAME']
#print members
exit()



