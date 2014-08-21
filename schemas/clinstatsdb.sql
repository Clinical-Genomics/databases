SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `datasource`;
CREATE TABLE `datasource` (
  `datasource_id` INT(11) NOT NULL AUTO_INCREMENT,
  `supportparams_id` INT(11) NOT NULL,
  `document_path` VARCHAR(255) NOT NULL,  
  `document_type` ENUM('html', 'xml', 'undefined') NOT NULL DEFAULT 'html',
  PRIMARY KEY (`datasource_id`),
  CONSTRAINT `datasource_ibfk_1` FOREIGN KEY (`supportparams_id`) REFERENCES `supportparams` (`supportparams_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `supportparams`;
CREATE TABLE `supportparams` (
  `supportparams_id` INT(11) NOT NULL AUTO_INCREMENT,
  `document_path` VARCHAR(255) NOT NULL,
  `systempid` VARCHAR(255),  
  `systemos` VARCHAR(255),
  `systemperlv` VARCHAR(255),  
  `systemperlexe` VARCHAR(255),
  `idstring` VARCHAR(255),  
  `program` VARCHAR(255),
  `commandline` TEXT,
  `sampleconfig_path` VARCHAR(255),
  `sampleconfig` TEXT,
  PRIMARY KEY (`supportparams_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `barcodelane`;
CREATE TABLE `barcodelane` (
  `barcodelane_id` INT(11) NOT NULL AUTO_INCREMENT,
  `datasource_id` INT(11) NOT NULL,
  `referencegenome_id` int(11),
  `sample_id` INT(11) DEFAULT NULL,
  `lane` INT(255),  
  `analysistype` VARCHAR(255),  
  `length` VARCHAR(255),
  `numtiles` INT(11),  
  PRIMARY KEY (`barcodelane_id`),
  CONSTRAINT `barcodelane_ibfk_1` FOREIGN KEY (`referencegenome_id`) REFERENCES `referencegenome`(`referencegenome_id`),
  CONSTRAINT `barcodelane_ibfk_2` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`sample_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `referencegenome`;
CREATE TABLE `referencegenome` (
  `referencegenome_id` INT(11) NOT NULL AUTO_INCREMENT,
  `referencegenome` VARCHAR(255) NOT NULL,
  `genomedirectory` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`referencegenome_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `sample`;
CREATE TABLE `sample` (
  `sample_id` INT(11) NOT NULL AUTO_INCREMENT,
  `project_id` INT(11) NOT NULL,
  `datasource_id` INT(11) NOT NULL,
  `samplename` VARCHAR(255) NOT NULL,  
  `barcode` VARCHAR(255),
  PRIMARY KEY (`sample_id`),
  CONSTRAINT `sample_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`),
  CONSTRAINT `sample_ibfk_2` FOREIGN KEY (`datasource_id`) REFERENCES `datasource` (`datasource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `project_id` INT(11) NOT NULL AUTO_INCREMENT,
  `datasource_id` INT(11) NOT NULL,
  `projectname` VARCHAR(255) NOT NULL,  
  `comment` TEXT,
  `time` DATETIME,
  PRIMARY KEY (`project_id`),
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`datasource_id`) REFERENCES `datasource` (`datasource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `flowcell`;
CREATE TABLE `flowcell` (
  `flowcell_id` INT(11) NOT NULL AUTO_INCREMENT,
  `datasource_id` INT(11) NOT NULL,
  `flowcellname` VARCHAR(9) NOT NULL UNIQUE,  
  `flowcell_pos` ENUM('A','B') NOT NULL,
  `time_start` DATETIME DEFAULT NULL,
  `time_end` DATETIME DEFAULT NULL,
  `time` DATETIME DEFAULT NULL,
  PRIMARY KEY (`flowcell_id`),
  CONSTRAINT `flowcell_ibfk_1` FOREIGN KEY (`datasource_id`) REFERENCES `datasource` (`datasource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `flowcellalign`;
CREATE TABLE `flowcellalign` (
  `flowcellalign_id` INT(11) NOT NULL AUTO_INCREMENT,
  `flowcell_id` INT(11) NOT NULL,
  `datasource_id` INT(11) NOT NULL,
  `runfolder` VARCHAR(255),  
  `machine` VARCHAR(255) NOT NULL,
  `rawclusters` INT(11),
  `pfclusters` INT(11),
  `yield_mb` INT(11),
  `time` DATETIME DEFAULT NULL,
  PRIMARY KEY (`flowcellalign_id`),
  CONSTRAINT `flowcellalign_ibfk_1` FOREIGN KEY (`flowcell_id`) REFERENCES `flowcell` (`flowcell_id`),
  CONSTRAINT `flowcellalign_ibfk_2` FOREIGN KEY (`datasource_id`) REFERENCES `datasource` (`datasource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `summaryaligned`;
CREATE TABLE `summaryaligned` (
  `summaryaligned_id` int(11) NOT NULL AUTO_INCREMENT,
  `sample_id` INT(11) DEFAULT NULL,
  `datasource_id` INT(11) NOT NULL,
  `controlsoft` VARCHAR(255) DEFAULT NULL,
  `primarysoft` VARCHAR(255) DEFAULT NULL,
  `secondarysoft` VARCHAR(255) DEFAULT NULL,
  `read_no` INT(11) DEFAULT NULL,
  `clusters_raw` INT(11) DEFAULT NULL,
  `clusters_pf` INT(11) DEFAULT NULL,
  `1st_cycle_int_pf` INT(11) DEFAULT NULL,
  `int_20cycles_pf_pct` DECIMAL(10,5) DEFAULT NULL,
  `clusters_pf_pct` DECIMAL(10,5) DEFAULT NULL,
  `align_pf_pct` DECIMAL(10,5) DEFAULT NULL,
  `alignment_score` DECIMAL(10,5) DEFAULT NULL,
  `mismatch_rate_pct` DECIMAL(10,5) DEFAULT NULL,
  `q30_bases_pf_pct` DECIMAL(10,5) DEFAULT NULL,
  `mean_quality_score_pf` DECIMAL(10,5) DEFAULT NULL,
  `pct_phasing` DECIMAL(10,5) DEFAULT NULL,
  `pct_prephasing` DECIMAL(10,5) DEFAULT NULL,
  `cycle2-4avint_pf` DECIMAL(10,5) DEFAULT NULL,
  `cycle2-10avpctloss_pf` DECIMAL(10,5) DEFAULT NULL,
  `cycle10-20avpctloss_pf` DECIMAL(10,5) DEFAULT NULL,
  PRIMARY KEY (`summaryaligned_id`),
  CONSTRAINT `summaryaligned_ibfk_1` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`sample_id`),
  CONSTRAINT `summaryaligned_ibfk_2` FOREIGN KEY (`datasource_id`) REFERENCES `datasource` (`datasource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `alignedfragments`;
CREATE TABLE `alignedfragments` (
  `alignedfragments_id` int(11) NOT NULL AUTO_INCREMENT,
  `sample_id` INT(11) DEFAULT NULL,
  `datasource_id` INT(11) NOT NULL,
  `fminus` INT(11) DEFAULT NULL,
  `fminus_pct` DECIMAL(10,5) DEFAULT NULL,
  `fplus` INT(11) DEFAULT NULL,
  `fplus_pct` DECIMAL(10,5) DEFAULT NULL,
  `rminus` INT(11) DEFAULT NULL,
  `rminus_pct` DECIMAL(10,5) DEFAULT NULL,
  `rplus` INT(11) DEFAULT NULL,
  `rplus_pct` DECIMAL(10,5) DEFAULT NULL,
  `total` INT(11) DEFAULT NULL,
  `median` INT(11) DEFAULT NULL,
  `belowmediansd` INT(11) DEFAULT NULL,
  `abovemediansd` INT(11) DEFAULT NULL,
  `lowtresh` INT(11) DEFAULT NULL,
  `hightresh` INT(11) DEFAULT NULL,
  `toosmall` INT(11) DEFAULT NULL,
  `toosmall_pct` DECIMAL(10,5) DEFAULT NULL,
  `toolarge` INT(11) DEFAULT NULL,
  `toolarge_pct` DECIMAL(10,5) DEFAULT NULL,
  `orisizeok` INT(11) DEFAULT NULL,
  `orisizeok_pct` DECIMAL(10,5) DEFAULT NULL,
  PRIMARY KEY (`alignedfragments_id`),
  CONSTRAINT `alignedfragments_ibfk_1` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`sample_id`),
  CONSTRAINT `alignedfragments_ibfk_2` FOREIGN KEY (`datasource_id`) REFERENCES `datasource` (`datasource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `unaligned`;
CREATE TABLE `unaligned` (
  `unaligned_id` int(11) NOT NULL AUTO_INCREMENT,
  `datasource_id` INT(11) NOT NULL,
  `sample_id` int(11) DEFAULT NULL,
  `flowcell_id` int(11) NOT NULL,
  `lane` int(11) DEFAULT NULL,
  `yield_mb` int(11) DEFAULT NULL,
  `passed_filter_pct` decimal(10,5) DEFAULT NULL,
  `readcounts` int(11) DEFAULT NULL,
  `raw_clusters_per_lane_pct` decimal(10,5) DEFAULT NULL,
  `perfect_indexreads_pct` decimal(10,5) DEFAULT NULL,
  `q30_bases_pct` decimal(10,5) DEFAULT NULL,
  `mean_quality_score` decimal(10,5) DEFAULT NULL,
  PRIMARY KEY (`unaligned_id`),
  UNIQUE KEY `unaligned_ibuk_1` (`flowcell_id`,`sample_id`,`lane`),
  CONSTRAINT `unaligned_ibfk_1` FOREIGN KEY (`datasource_id`) REFERENCES `datasource` (`datasource_id`),
  CONSTRAINT `unaligned_ibfk_2` FOREIGN KEY (`flowcell_id`) REFERENCES `flowcell` (`flowcell_id`),
  CONSTRAINT `unaligned_ibfk_3` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`sample_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS = 1;
