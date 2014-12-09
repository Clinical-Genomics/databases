#!/usr/bin/python
#Script that connects to the MySQL database and parses data from an html table
#Import the mysql.connector library/module
#
#  from the bash script starting qc parsing to db
#  /home/clinical/SCRIPTS/parseunaligned_dbserver.py /home/clinical/DEMUX/${RUN}/ /home/clinical/RUNS/${RUN}/Data/Intensities/BaseCalls/SampleSheet.csv
#
import sys
import MySQLdb as mysql
from bs4 import BeautifulSoup
import time
import glob
import re
import socket
import os

if (len(sys.argv)>1):
  basedir = sys.argv[1]
else:
  message = ("usage: "+sys.argv[0]+" <BASEDIRECTORYforUNALIGNED> <absolutepathtosamplesheetcsv> <config_file:optional>")
  sys.exit(message)

configfile = "/home/hiseq.clinical/.scilifelabrc"
if (len(sys.argv)>3):
  if os.path.isfile(sys.argv[3]):
    configfile = sys.argv[3]
    
params = {}
with open(configfile, "r") as confs:
  for line in confs:
    if len(line) > 5 and not line[0] == "#":
      line = line.rstrip()
      pv = line.split(" ")
      params[pv[0]] = pv[1]

