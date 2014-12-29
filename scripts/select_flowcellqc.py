#!/usr/bin/python
#Script that connects to the MySQL database and parses data from an html table
#Import the mysql.connector library/module
#
#  from the bash script starting qc parsing to db
#  /home/clinical/SCRIPTS/parseunaligned_dbserver.py /home/clinical/DEMUX/${RUN}/ 
#                                       /home/clinical/RUNS/${RUN}/Data/Intensities/BaseCalls/SampleSheet.csv
#
import sys
import MySQLdb as mysql
#from bs4 import BeautifulSoup
import time
import glob
import re
import socket
import os

# this script is written for database version:
_MAJOR_ = 1
_MINOR_ = 0
_PATCH_ = 1

configfile = "/home/hiseq.clinical/.scilifelabrc"
if (len(sys.argv)>1):
  if os.path.isfile(sys.argv[1]):
    configfile = sys.argv[1]
    
params = {}
with open(configfile, "r") as confs:
  for line in confs:
    if len(line) > 5 and not line[0] == "#":
      line = line.rstrip()
      pv = line.split(" ")
      params[pv[0]] = pv[1]


now = time.strftime('%Y-%m-%d %H:%M:%S')
cnx = mysql.connect(user=params['CLINICALDBUSER'], port=int(params['CLINICALDBPORT']), host=params['CLINICALDBHOST'], 
                    passwd=params['CLINICALDBPASSWD'], db=params['STATSDB'])
cursor = cnx.cursor()

cursor.execute(""" SELECT major, minor, patch FROM version ORDER BY time DESC LIMIT 1 """)
row = cursor.fetchone()
if row is not None:
  major = row[0]
  minor = row[1]
  patch = row[2]
else:
  sys.exit("Incorrect DB, version not found.")
if (major == _MAJOR_ and minor == _MINOR_ and patch == _PATCH_):
  print "Correct database " + params['STATSDB'] + "  version "+str(_MAJOR_)+"."+str(_MINOR_)+"."+str(_PATCH_)
else:
  exit (params['STATSDB'] + " - Incorrect DB version. This script is made for "+str(_MAJOR_)+"."+str(_MINOR_)+"."+str(_PATCH_) +
      " not for " + str(major)+"."+str(minor)+"."+str(patch))

yourreply = raw_input("\n\tIs this the correct database? YES/[no] ")
if yourreply != "YES":
  exit()

cursor.execute(""" SELECT YEAR(rundate) AS year, MONTH(rundate) AS month, COUNT(DISTINCT datasource.datasource_id) AS runs, 
                   ROUND(SUM(readcounts)/2000000, 2) AS "mil reads", 
                   ROUND(SUM(readcounts)/(2000000*COUNT(DISTINCT datasource.datasource_id)),1) AS "mil reads/fc lane"
                  FROM datasource 
                  LEFT JOIN flowcell ON datasource.datasource_id = flowcell.datasource_id 
                  LEFT JOIN unaligned ON unaligned.flowcell_id = flowcell.flowcell_id 
                  GROUP BY YEAR(rundate), MONTH(rundate)
                  ORDER BY YEAR(rundate), MONTH(rundate), DAY(rundate); """)
if not cursor.fetchone():
  print "Nothing found"
else:
  print "YEAR MM runs Mreads reads/fc lane"
  rows = cursor.fetchall()
  for row in rows:
    print row[0], row[1], row[2], row[3], row[4]

completeflowcells = """ SELECT runname, COUNT(DISTINCT datasource.datasource_id) AS runs, 
                   flowcellname, lane, SUM(readcounts),
                   ROUND(SUM(readcounts)/(2000000),1) AS "mil reads/fc lane",
                   GROUP_CONCAT(q30_bases_pct*readcounts), datasource.datasource_id, rundate
                  FROM datasource 
                  LEFT JOIN flowcell ON datasource.datasource_id = flowcell.datasource_id 
                  LEFT JOIN unaligned ON unaligned.flowcell_id = flowcell.flowcell_id 
                  GROUP BY unaligned.flowcell_id, lane 
                  ORDER BY rundate, flowcellname, lane """
onlydemuxsamples = """ SELECT runname, COUNT(DISTINCT datasource.datasource_id) AS runs, 
                   flowcellname, lane, SUM(readcounts),
                   ROUND(SUM(readcounts)/(2000000),1) AS "mil reads/fc lane",
                   GROUP_CONCAT(q30_bases_pct*readcounts), datasource.datasource_id, rundate
                  FROM sample, datasource 
                  LEFT JOIN flowcell ON datasource.datasource_id = flowcell.datasource_id 
                  LEFT JOIN unaligned ON unaligned.flowcell_id = flowcell.flowcell_id 
                  WHERE sample.sample_id = unaligned.sample_id
                  AND samplename NOT IN ('lane1', 'lane2')
                  GROUP BY unaligned.flowcell_id, lane 
                  ORDER BY rundate, flowcellname, lane """

cursor.execute(completeflowcells)
if not cursor.fetchone():
  print "Nothing found"
else:
  print "start runname cnt fc lane readcounts Mreads/lane Q30 runid reads>Q30"
  rows = cursor.fetchall()
  for row in rows:
    q30joined = row[6].split(',')
    q30sum = 0
    for q30s in q30joined:
      q30sum += float(q30s)
    if int(row[4]) > 0:
      fcq30 = q30sum/int(row[4])
    else:
      fcq30 = 0
    print row[8], row[0], row[1], row[2], row[3], row[4], row[5], "{0:.2f}".format(fcq30), row[7], "{0:.2f}".format(float(row[5])*float(fcq30)/100)



exit(0)
