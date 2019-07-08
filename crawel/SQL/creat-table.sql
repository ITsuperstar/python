CREATE TABLE `fund`.`fund3` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person` varchar(45) DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `money` varchar(45) DEFAULT NULL,
  `project_id` varchar(45) DEFAULT NULL,
  `project_type` varchar(45) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `approval_year` varchar(45) DEFAULT NULL,
  `subject` varchar(200) DEFAULT NULL,
  `subject_classification` varchar(200) DEFAULT NULL,
  `subject_code` varchar(200) DEFAULT NULL,
  `execution_time` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=168892 DEFAULT CHARSET=utf8;