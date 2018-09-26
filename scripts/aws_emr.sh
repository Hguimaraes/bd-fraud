# Create a Hive table from RDS
sqoop import --connect "jdbc:mysql://ifds-rds.cmi2faravii8.sa-east-1.rds.amazonaws.com:3306/ifds" \
--username hguimaraes -P --table hist_data  --hive-import --create-hive-table --hive-table HIST_DATA \
--delete-target-dir --target-dir /user/hadoop/HIST_DATA --hive-overwrite -m 4

# Move stream data to HDFS
hadoop distcp s3n://ita-bd-fds/data/data/pays_test.csv /user/ita-fds/

# Install Git on EMR
sudo yum install git
git clone https://github.com/Hguimaraes/bd-fraud

# Install dependencies
sudo pip-3.4 install cherrypy flask paste

# Change pyspark_python variable 
sudo vim /usr/lib/spark/conf/spark-env.sh
# INSERT: export PYSPARK_PYTHON=python3

# Go to src directory
cd bd-fraud
cd src

# Initialize spark
spark-submit --total-executor-cores 6 --executor-memory 4g server.py