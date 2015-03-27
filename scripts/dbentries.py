#!/usr/bin/python
#
import sys
import os
import time
from access import db

"""Counts database entries.
  usage: dbentries.py <config_file:optional>
  Will list tables and count entries
Args:
  config_file (str): name of config file
Returns:
  Counts all table entries
"""

if (len(sys.argv)>1):
  configfile = sys.argv[1]
  if not os.path.isfile(configfile):
    exit("Bad configfile")
else:
  if len(sys.argv) == 1:
    configfile = 'None'
  else:
    print "usage: dbentries.py <config_file:optional>"
    exit(1)
pars = db.readconfig(configfile)

with db.create_tunnel(pars['TUNNELCMD']):

  with db.dbconnect(pars['CLINICALDBHOST'], pars['CLINICALDBPORT'], pars['STATSDB'], 
                        pars['CLINICALDBUSER'], pars['CLINICALDBPASSWD']) as dbc:

    ver = dbc.versioncheck(pars['STATSDB'], pars['DBVERSION'])

    if not ver == 'True':
      print "Wrong db " + pars['STATSDB'] + " v:" + pars['DBVERSION']
      exit(0) 
    else:
      print "Correct db " + pars['STATSDB'] + " v:" + pars['DBVERSION']

    tablequery = """ SHOW TABLES """
    alltables = dbc.generalquery(tablequery)
    print "TABLE rowcount"
    if alltables:
#      print str(alltables)
      for num in range(len(alltables)):
#        print alltables[num]
        for key in alltables[num]:
#          print alltables[num][key]
          query = """ SELECT COUNT(*) AS cnt FROM """ + alltables[num][key] + """ """
          count = dbc.generalquery(query)
          if count:
            print alltables[num][key], str(int(count[0]['cnt']))

    namequery = """ SELECT COUNT(sample_id) AS cnt, samplename AS name, group_concat(sample_id) AS ids 
                 FROM sample GROUP BY samplename ORDER BY cnt DESC LIMIT 5; """
    names = dbc.generalquery(namequery)
    print "NAME COUNT IDs"
    if names:
#      print str(alltables)
      for num in range(len(names)):
#        print alltables[num]
#        for key in names[num]:
#          print alltables[num][key]
        print names[num][name], names[num][cnt], names[num][ids] 





#print "\n\tcontent of 'clinstatsdb'  " + now
#for tabell in ['datasource', 'flowcell', 'project', 'sample', 'supportparams', 'unaligned']:
#  cursor.execute(""" SELECT COUNT(*) FROM """ + tabell)
#  if not cursor.fetchone():
#    print "Table " + tabell + " not found . . . "
#  else:
#    cursor.execute(""" SELECT COUNT(*) FROM """ + tabell)
#    match = cursor.fetchone()
#    print "\t%15s %6d" % (tabell, match[0])
#print "\n"
