#!/usr/bin/python
#
import sys
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
else:
  if len(sys.argv) == 2:
    configfile = 'None'
  else:
    print "usage: deleteflowcell.py <flowcellname> <config_file:optional>"
    exit(1)
pars = db.readconfig(configfile)

