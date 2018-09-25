# Create a Hive table from RDS
sqoop import --connect "jdbc:mysql://ifds-rds.cmi2faravii8.sa-east-1.rds.amazonaws.com:3306/ifds" \
--username hguimaraes -P --table hist_data  --hive-import --create-hive-table --hive-table HIST_DATA \
--delete-target-dir --target-dir /user/hadoop/HIST_DATA --hive-overwrite -m 4

# Move stream data to HDFS
