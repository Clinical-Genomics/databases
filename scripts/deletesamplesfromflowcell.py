#!/usr/bin/python
#Script that connects to the MySQL database and parses data from an html table
#Import the mysql.connector library/module
import sys
import MySQLdb as mysql
#from bs4 import BeautifulSoupi
import os.path
import time
import glob
import re

if (len(sys.argv)>1):
  fcname = sys.argv[1]
else:
  message = ("usage: "+sys.argv[0]+" <flowcell-name> <config_file:optional>")
  sys.exit(message)

configfile = "/home/hiseq.clinical/.scilifelabrc"
if (len(sys.argv)>2):
  if os.path.isfile(sys.argv[2]):
    configfile = sys.argv[2]
    
params = {}
with open(configfile, "r") as confs:
  for line in confs:
    if len(line) > 5 and not line[0] == "#":
      line = line.rstrip()
      pv = line.split(" ")
      params[pv[0]] = pv[1]

now = time.strftime('%Y-%m-%d %H:%M:%S')
# this script is written for database version:
_VERSION_ = params['DBVERSION']
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
if (str(major)+"."+str(minor)+"."+str(patch) == _VERSION_):
  print "Correct database "+str(_VERSION_)
else:
  exit ("Incorrect DB version. This script is made for "+str(_VERSION_)+" not for "+str(major)+"."+str(minor)+"."+str(patch))

print ("\n\tFC: "+fcname+"    DATABASE IS "+params['STATSDB']+"  ver "+_VERSION_+"\n")

cursor.execute(""" SELECT project.projectname, flowcell.flowcellname, sample.samplename, unaligned.lane, 
unaligned.readcounts, unaligned.yield_mb, TRUNCATE(q30_bases_pct,2), TRUNCATE(mean_quality_score,2),
flowcell.flowcell_id, sample.sample_id, unaligned.unaligned_id, datasource.datasource_id, datasource.document_path,
supportparams.supportparams_id
FROM sample, flowcell, unaligned, project, datasource, supportparams
WHERE sample.sample_id     = unaligned.sample_id
AND   flowcell.flowcell_id = unaligned.flowcell_id
AND   sample.project_id    = project.project_id 
AND   datasource.datasource_id = flowcell.datasource_id
AND   datasource.supportparams_id = supportparams.supportparams_id
AND   flowcellname = '""" + fcname + """'
ORDER BY flowcellname, sample.samplename, lane """)
data = cursor.fetchall()
FCs = []
smpls = []
unals = []
srcs = []
srid = []
sprtps = []

if data:
  print "Project\tFlowcell\tSample\tLane\tRead counts\tyieldMB\t%Q30\tMeanQscore\tsource_id"
else:
  print "Flowcell " + fcname + " not found . . ."
for row in data:
  print row[0]+"\t"+row[1]+"\t"+str(row[2])+"\t"+str(row[3])+"\t"+str(row[4])+"\t"+str(row[5])+"\t"+str(row[6])+"\t"+str(row[7])+"\t"+str(row[11])
  try:
    exist = FCs.index(row[8])
  except ValueError:
    FCs.append(row[8])
  else:
    "Already added"
  try:
    exist = smpls.index(row[9])
  except ValueError:
    smpls.append(row[9])
  else:
    "Already added"
  try:
    exist = unals.index(row[10])
  except ValueError:
    unals.append(row[10])
  else:
    "Already added"
  try:
    exist = srcs.index(row[12])
  except ValueError:
    srcs.append(row[12])
  else:
    "Already added"
  try:
    exist = srid.index(row[11])
  except ValueError:
    srid.append(row[11])
  else:
    "Already added"
  try:
    exist = sprtps.index(row[13])
  except ValueError:
    sprtps.append(row[13])
  else:
    "Already added"

print "\n\tFound " + str(len(FCs)) + " flowcells, " + str(FCs).replace("L", "")
print "\tFound " + str(len(unals)) + " unaligned rows, " + str(unals).replace("L", "")
print "\tFound " + str(len(smpls)) + " samples, " + str(smpls).replace("L", "")
print "\tFound " + str(len(srcs)) + " sources, " + str(srcs).replace("L", "") + " ids " + str(srid).replace("L", "")
print "\tFound " + str(len(sprtps)) + " supportps, " + str(sprtps).replace("L", "")

_samples_ = str(smpls).replace('L', "").replace('[', "").replace(']', "")
_unalgns_ = str(unals).replace('L', "").replace('[', "").replace(']', "")
query0 = """ SELECT samplename, sample.sample_id, unaligned_id, lane, flowcell_id FROM sample, unaligned 
            WHERE sample.sample_id = unaligned.sample_id 
            AND sample.sample_id IN ("""+_samples_+""")
           AND NOT unaligned_id IN ("""+_unalgns_+""") """
query = """ SELECT samplename, sample.sample_id, GROUP_CONCAT(unaligned_id), 
            COUNT(DISTINCT unaligned_id), COUNT(DISTINCT flowcell_id) FROM sample, unaligned 
            WHERE sample.sample_id = unaligned.sample_id 
            AND sample.sample_id IN ("""+_samples_+""")
           AND NOT unaligned_id IN ("""+_unalgns_+""") 
           GROUP BY sample.sample_id  """
#cursor.execute(query)
#reply = cursor.fetchall()
#for row in reply:
#  print row[0], row[1], row[2], row[3], row[4] 
#  # now we keep all sample_ids that have statistics from other flowcells
#  if row[1] in smpls:
#    smpls.remove(row[1])
#    print row[1], smpls

yourreply = raw_input("\n\tDO YOU want to delete these statistics from the database? YES/[no] ")

if yourreply == "YES":
  print "\n\t" + yourreply
  yourreply = "no"
  yourreply = raw_input("\tARE YOU sure the data will now be deleted? YES/[no] ")
  if yourreply == "YES":
    print "\n\t" + yourreply
  else:
    print "\tnehe, will exit . .\n"
    cursor.close()
    cnx.close()
    exit(0)
else:
  print "\tnehe, will exit . .\n"
  cursor.close()
  cnx.close()
  exit(0)

print "Will delete unaligned"
for f in unals:
  try:
    cursor.execute(""" DELETE FROM unaligned WHERE unaligned_id = '{0}' """.format(f))
  except mysql.IntegrityError, e: 
    print "Error %d: %s" % (e.args[0],e.args[1])
    exit("DB error")
  except mysql.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    exit("Syntax error")
  except mysql.Warning, e:
    print "Warning %d: %s" % (e.args[0],e.args[1])
    exit("MySQL warning")
  cnx.commit()
  print "Unaligned id " + str(f) + " deleted "

print "Will delete sample (if not present on other flowcells)"
for f in smpls:
  query = """ SELECT unaligned_id, flowcellname FROM flowcell, unaligned 
                     WHERE flowcell.flowcell_id = unaligned.flowcell_id AND sample_id = '{0}' """.format(f)
#  print query
  cursor.execute(query)
  data = cursor.fetchall()
  if data:  
    for ff in data:
      if (f != 18 and f != 19):
        print "Found sample_id "+str(f)+" unaligned_id: "+str(ff[0])+" from fc "+ff[1]
  else:
    try:
      cursor.execute(""" DELETE FROM sample WHERE sample_id = '{0}' """.format(f))
    except mysql.IntegrityError, e:      
      print "Error %d: %s" % (e.args[0],e.args[1])
      exit("DB error")
    except mysql.Error, e:
      print "Error %d: %s" % (e.args[0],e.args[1])
      exit("Syntax error")
    except mysql.Warning, e:
      print "Warning %d: %s" % (e.args[0],e.args[1])
      exit("MySQL warning")
    cnx.commit()
    print "Sample id " + str(f) + " [unaligned not found] - deleted "

print "Will delete flowcell"
for f in FCs:
  try:
    cursor.execute(""" DELETE FROM flowcell WHERE flowcell_id = '{0}' """.format(f))
  except mysql.IntegrityError, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    exit("DB error")
  except mysql.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    exit("Syntax error")
  except mysql.Warning, e:
    print "Warning %d: %s" % (e.args[0],e.args[1])
    exit("MySQL warning")
  cnx.commit()
  print "FC " + str(f) + " deleted "

print "Will delete datasource"
for f in srid:
  try:
    cursor.execute(""" DELETE FROM datasource WHERE datasource_id = '{0}' """.format(f))
  except mysql.IntegrityError, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    exit("DB error")
  except mysql.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    exit("Syntax error")
  except mysql.Warning, e:
    print "Warning %d: %s" % (e.args[0],e.args[1])
    exit("MySQL warning")
  cnx.commit()
  print "Datasource id " + str(f) + " deleted "

print "Will delete supportparams"
for f in sprtps:
  try:
    cursor.execute(""" DELETE FROM supportparams WHERE supportparams_id = '{0}' """.format(f))
  except mysql.IntegrityError, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    exit("DB error")
  except mysql.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    exit("Syntax error")
  except mysql.Warning, e:
    print "Warning %d: %s" % (e.args[0],e.args[1])
    exit("MySQL warning")
  cnx.commit()
  print "Supportparams id " + str(f) + " deleted "

cnx.commit()
cursor.close()
cnx.close()
print "    done!"

