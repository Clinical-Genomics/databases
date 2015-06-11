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
      for num in range(len(alltables)):
        for key in alltables[num]:
          query = """ SELECT COUNT(*) AS cnt FROM """ + alltables[num][key] + """ """
          count = dbc.generalquery(query)
          if count:
            print alltables[num][key], str(int(count[0]['cnt']))

    namequery = """ SELECT COUNT(sample_id) AS cnt, samplename AS name, group_concat(sample_id) AS ids 
                 FROM sample GROUP BY samplename ORDER BY cnt DESC LIMIT 5; """
    names = dbc.generalquery(namequery)
    print "NAME COUNT IDs"
    if names:
      for num in range(len(names)):
        if names[num]['cnt'] > 1:
          print names[num]['name'], names[num]['cnt'], names[num]['ids'], ' - - - W A R N I N G !'
        else:
          print names[num]['name'], names[num]['cnt'], names[num]['ids'], 'ok'


