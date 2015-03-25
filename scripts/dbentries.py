#!/usr/bin/python
#
import sys
import os
import time
from access import db

"""Removes flowcell/demux from db.
  usage: deleteflowcell.py  <flowcellname> <config_file:optional>
  Will list all demux from flowcell allowing user to chose which ones to delete
Args:
  flowcellname (str): name of flowcell containing demux stats to delete
Returns:
  Prints out all changes to the database
"""

if (len(sys.argv)>2):
  configfile = sys.argv[2]
  if not os.path.isfile(configfile):
    exit("Bad configfile")
  fcname = sys.argv[1]
else:
  if len(sys.argv) == 2:
    configfile = 'None'
    fcname = sys.argv[1]
  else:
    print "usage: deleteflowcell.py <flowcellname> <config_file:optional>"
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
