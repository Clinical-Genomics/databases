#!/usr/bin/python
#Script that connects to the MySQL database and parses data from an html table
#Import the mysql.connector library/module
import sys
import MySQLdb as mysql
import time
import glob
import re
import getpass

params = {}
with open("/home/hiseq.clinical/.scilifelabrc", "r") as confs:
  for line in confs:
    if len(line) > 5 and not line[0] == "#":
      line = line.rstrip()
      pv = line.split(" ")
      params[pv[0]] = pv[1]

now = time.strftime('%Y-%m-%d %H:%M:%S')
cnx = mysql.connect(user=params['CLINICALDBUSER'], port=int(params['CLINICALDBPORT']), host=params['CLINICALDBHOST'], 
      passwd=params['CLINICALDBPASSWD'], db=params['STATSDB'])
cursor = cnx.cursor()

print "\n\tcontent of 'clinstatsdb'  " + now
for tabell in ['datasource', 'flowcell', 'project', 'sample', 'supportparams', 'unaligned']:
  cursor.execute(""" SELECT COUNT(*) FROM """ + tabell)
  if not cursor.fetchone():
    print "Table " + tabell + " not found . . . "
  else:
    cursor.execute(""" SELECT COUNT(*) FROM """ + tabell)
    match = cursor.fetchone()
    print "\t%15s %6d" % (tabell, match[0])
print "\n"

