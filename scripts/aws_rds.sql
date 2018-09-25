-- Start instance as
-- mysql -h ifds-rds.cmi2faravii8.sa-east-1.rds.amazonaws.com -P 3306 -u hguimaraes -p --local-infile=1

CREATE TABLE `ifds`.`hist_data` (
  `paysim_id` INT NOT NULL AUTO_INCREMENT,
  `step` INT NULL,
  `type` VARCHAR(255) NULL,
  `amount` FLOAT NULL,
  `nameOrig` VARCHAR(255) NULL,
  `oldbalanceOrg` FLOAT NULL,
  `newbalanceOrig` FLOAT NULL,
  `nameDest` VARCHAR(255) NULL,
  `oldbalanceDest` FLOAT NULL,
  `newbalanceDest` FLOAT NULL,
  `isFraud` INT NULL,
  `isFlaggedFraud` INT NULL,
  PRIMARY KEY (`paysim_id`));


LOAD DATA LOCAL INFILE 'C:\\Users\\heito\\Documents\\CEDS841\\pays_train.csv' \
INTO TABLE ifds.hist_data FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 \
LINES (step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud);