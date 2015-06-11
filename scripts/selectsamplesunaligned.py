#!/usr/bin/python
#Script that connects to the MySQL database and parses data from an html table
#Import the mysql.connector library/module
import sys
import MySQLdb as mysql
from bs4 import BeautifulSoup
import time
import glob
import re

now = time.strftime('%Y-%m-%d %H:%M:%S')
cnx = mysql.connect(user='username', port=port, host='hostname', passwd='password', db='databasename')
cursor = cnx.cursor()

# SELECT stats
#proje = sys.argv[1]
#flowc = sys.argv[2]
if len(sys.argv) == 2:
  smpls = sys.argv[1]
else:
  print ("\n\tUsage: "+sys.argv[0]+" samplelist.txt\n")
  exit()

print ("S: "+smpls)

try:
  with open(smpls) as f:
    lines = []
    for line in f:
      line = line.rstrip()
      if (line != ''):
        lines.append(line)
except IOError:
  print ("Could not read "+smpls)
  exit()

smps = ''
for lin in lines:
  smps = smps+"','"+lin

smps = "'"+smps.lstrip("','")+"'"
print smps
#smps = ','.join(str(x) for x in smps)

cursor.execute(""" SELECT project.projectname, flowcell.flowcellname, sample.samplename, unaligned.lane, 
unaligned.readcounts, unaligned.yield_mb, TRUNCATE(q30_bases_pct,2), TRUNCATE(mean_quality_score,2)
FROM sample, flowcell, unaligned, project
WHERE sample.sample_id     = unaligned.sample_id
AND   flowcell.flowcell_id = unaligned.flowcell_id
AND   sample.project_id    = project.project_id 
AND   samplename IN( """ + smps + """ )
ORDER BY flowcellname, sample.samplename, lane """)
data = cursor.fetchall()
print "Project\tFlowcell\tSample\tLane\tRead counts\tyieldMB\t%Q30\tMeanQscore"
for row in data:
  print row[0]+"\t"+row[1]+"\t"+str(row[2])+"\t"+str(row[3])+"\t"+str(row[4])+"\t"+str(row[5])+"\t"+str(row[6])+"\t"+str(row[7])


cursor.close()
cnx.close()


