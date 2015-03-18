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
      basemask
      FROM sample, flowcell, unaligned, project, datasource, supportparams, demux
      WHERE sample.sample_id     = unaligned.sample_id
      AND   flowcell.flowcell_id = demux.flowcell_id
      AND   demux.demux_id = unaligned.demux_id
      AND   sample.project_id    = project.project_id 
      AND   datasource.datasource_id = demux.datasource_id
      AND   datasource.supportparams_id = supportparams.supportparams_id
      AND   flowcellname = '""" + fcname + """'
      ORDER BY flowcellname, sample.samplename, lane """
    print totalquery

    allhits = dbc.generalquery(totalquery)
    for hit in allhits:
      print hit['smp'], hit['basemask'], hit['lane']


