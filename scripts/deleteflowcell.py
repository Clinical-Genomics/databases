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

    print fcname
    totalquery = """ SELECT project.projectname AS prj, flowcell.flowcellname AS flc, sample.samplename AS smp, 
      unaligned.lane AS lane, unaligned.readcounts AS rc, unaligned.yield_mb AS yield, TRUNCATE(q30_bases_pct,2) AS q30, 
      TRUNCATE(mean_quality_score,2) AS meanq, flowcell.flowcell_id AS flcid, sample.sample_id AS smpid, 
      unaligned.unaligned_id AS unalid, datasource.datasource_id AS dsid, datasource.document_path AS docpath,
      supportparams.supportparams_id AS supportid, project.project_id AS prjid, supportparams.document_path AS suppath,
      basemask, demux.demux_id AS demuxid
      FROM sample, flowcell, unaligned, project, datasource, supportparams, demux
      WHERE sample.sample_id     = unaligned.sample_id
      AND   flowcell.flowcell_id = demux.flowcell_id
      AND   demux.demux_id = unaligned.demux_id
      AND   sample.project_id    = project.project_id 
      AND   datasource.datasource_id = demux.datasource_id
      AND   datasource.supportparams_id = supportparams.supportparams_id
      AND   flowcellname = '""" + fcname + """'
      ORDER BY flowcellname, demuxid, sample.samplename, lane """
#    print totalquery

    allhits = dbc.generalquery(totalquery)
#    for hit in allhits:
#      print hit['smp'], hit['basemask'], hit['lane'], hit['demuxid']

    FCs = []
    smpls = []
    unals = []
    srcs = []
    srid = []
    sprtps = []
    sprtids = []
    projs = []
    dmxs = []
    bms = []

    if allhits:
      print "Project\tFlowcell\tbasemask\tSample\tLane\tRead counts\tyieldMB\t%Q30\tMeanQscore\tsource_id\tproject_id"
    else:
      print "Flowcell " + fcname + " not found . . ."
    for row in allhits:
      print (row['prj'] + "\t" + row['flc'] + "\t" + row['basemask'] + "\t" + row['smp'] + "\t" + str(row['lane']) + "\t" +
             str(row['rc']) + "\t" + str(row['yield']) + "\t" + str(row['q30']) + "\t" + str(row['meanq']) + "\t" + 
             str(row['dsid']) + "\t" + str(row['prjid']))
      try:
        exist = FCs.index(row['flcid'])
      except ValueError:
        FCs.append(row['flcid'])
      else:
        "Already added"
      try:
        exist = smpls.index(row['smpid'])
      except ValueError:
        smpls.append(row['smpid'])
      else:
        "Already added"
      try:
        exist = unals.index(row['unalid'])
      except ValueError:
        unals.append(row['unalid'])
      else:
        "Already added"
      try:
        exist = srcs.index(row['docpath'])
      except ValueError:
        srcs.append(row['docpath'])
      else:
        "Already added"
      try:
        exist = srid.index(row['dsid'])
      except ValueError:
        srid.append(row['dsid'])
      else:
        "Already added"
      try:
        exist = sprtids.index(row['supportid'])
      except ValueError:
        sprtids.append(row['supportid'])
      else:
        "Already added"
      try:
        exist = projs.index(row['prjid'])
      except ValueError:
        projs.append(row['prjid'])
      else:
        "Already added"
      try:
        exist = sprtps.index(row['suppath'])
      except ValueError:
        sprtps.append(row['suppath'])
      else:
        "Already added"
      try:
        exist = dmxs.index(row['demuxid'])
      except ValueError:
        dmxs.append(row['demuxid'])
      else:
        "Already added"
      try:
        exist = bms.index(row['basemask'])
      except ValueError:
        bms.append(row['basemask'])
      else:
        "Already added"

print "\n\tFound " + str(len(FCs)) + " flowcells, " + str(FCs).replace("L", "")
for i in range(len(dmxs)):
  print "\tdemux " + str(dmxs[i]) + "  " + bms[i]
print "\tFound " + str(len(unals)) + " unaligned rows, " + str(unals).replace("L", "")
print "\tFound " + str(len(smpls)) + " samples, " + str(smpls).replace("L", "")
print "\tFound " + str(len(srcs)) + " sources, " + str(srcs).replace("L", "") + " ids " + str(srid).replace("L", "")
print "\tFound " + str(len(sprtps)) + " supportps, " + str(sprtps).replace("L", "") + " ids " + str(sprtids).replace("L", "")
print "\tFound " + str(len(projs)) + " projs, " + str(projs).replace("L", "")


print ("\n\t")
for i in range(len(dmxs)):
  print ("\tDo you want to delete [" + str(dmxs[i]) + "]  - " + bms[i])
print ("\tDo you want to delete the entire flowcell A?")
yourreply = raw_input("\n\tGive corresponding 'basemask no' or 'A' for all: ")

print yourreply

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



