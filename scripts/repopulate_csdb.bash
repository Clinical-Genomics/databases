#!/bin/bash
#   usage: repopulate_csdb.bash <path to demux root dir>

set -e

NOW=$(date +"%Y%m%d%H%M%S")
UNALIGNEDBASE=/home/clinical/DEMUX/
RUNBASE=/home/clinical/oldRUNS/

for DEMUXDIR in $@; do
  BASE=$(echo $DEMUXDIR | awk '{if (substr($0,length($0),1) != "/") {print $0"/"} else {print $0}}')
  RUN=$(echo ${BASE} | awk 'BEGIN {FS="/"} {print $(NF-1)}')
  FC=$(echo ${BASE} | awk 'BEGIN {FS="/"} {split($(NF-1),arr,"_");print substr(arr[4],2,length(arr[4]))}')
  
  # python /home/clinical/SCRIPTS/deleteflowcell.py $FC ~/.alt_test_test_db

  for UNALDIR in $(cd ${UNALIGNEDBASE}/${RUN}/ && ls -d Unaligned*); do
    echo "/home/hiseq.clinical/.virtualenv/mysql/bin/python /home/clinical/SCRIPTS/parsedemux.py ${UNALIGNEDBASE}/${RUN}/ ${UNALDIR}/ ${RUNBASE}/${RUN}/Data/Intensities/BaseCalls/SampleSheet.csv ~/.alt_test_test_db"
    /home/hiseq.clinical/.virtualenv/mysql/bin/python /home/clinical/SCRIPTS/parsedemux.py ${UNALIGNEDBASE}/${RUN}/ ${UNALDIR}/ ${RUNBASE}/${RUN}/Data/Intensities/BaseCalls/SampleSheet.csv ~/.alt_test_test_db
    
    PROJs=$(ls ${UNALIGNEDBASE}${RUN}/${UNALDIR}/ | grep Proj)
    for PROJ in ${PROJs[@]}; do
      prj=$(echo ${PROJ} | sed 's/Project_//')
      /home/hiseq.clinical/.virtualenv/mysql/bin/python /home/clinical/SCRIPTS/selectdemux.py ${prj} ${FC} ~/.alt_test_test_db >> ${UNALIGNEDBASE}${RUN}/${UNALDIR}/stats-${prj}-${FC}.txt.re
    done
  done
done  
