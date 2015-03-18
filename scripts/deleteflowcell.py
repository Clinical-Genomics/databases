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
    totalquery = """ SELECT project.projectname, flowcell.flowcellname, sample.samplename, unaligned.lane, 
      unaligned.readcounts, unaligned.yield_mb, TRUNCATE(q30_bases_pct,2), TRUNCATE(mean_quality_score,2),
      flowcell.flowcell_id, sample.sample_id, unaligned.unaligned_id, datasource.datasource_id, datasource.document_path,
      supportparams.supportparams_id, project.project_id, supportparams.document_path
      FROM sample, flowcell, unaligned, project, datasource, supportparams
      WHERE sample.sample_id     = unaligned.sample_id
      AND   flowcell.flowcell_id = unaligned.flowcell_id
      AND   sample.project_id    = project.project_id 
      AND   datasource.datasource_id = flowcell.datasource_id
      AND   datasource.supportparams_id = supportparams.supportparams_id
      AND   flowcellname = '""" + fcname + """'
      ORDER BY flowcellname, sample.samplename, lane """
    print totalquery

