
#!/usr/bin/python
#
import sys
import os
import glob
import time
import re
from access import db

"""Parses demux stats to db.
  usage: parsedemux.py  <BASEDIRECTORYforUNALIGNED> <UNALIGNEDsubdir> <samplesheetcsv> <config_file:optional>
Args:
  BASEDIRECTORYforUNALIGNED (str): path to demux directory
  UNALIGNEDsubdir (str): subdir with demux data structure
  pathtosamplesheetcsv (str): absolute path to samplesheet
Returns:
  Outputs what data have been added to database including row id for each table
"""

if (len(sys.argv)>4):
  configfile = sys.argv[4]
  if not os.path.isfile(configfile):
    exit("Bad configfile")
else:
  if len(sys.argv) == 4:
    configfile = 'None'
  else:
    print "usage: parsedemux.py <BASEDIRECTORYforUNALIGNED> <UNALIGNEDsubdir> <samplesheetcsv> <config_file:optional>"
    exit(1)
pars = db.readconfig(configfile)
