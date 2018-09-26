import os
import time
import logging
import threading
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.mllib.linalg import DenseVector
from pyspark.mllib.regression import LabeledPoint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
@description: Class to abstract all Spark computations
"""
class FraudEngine:
    """
    """
    def __init__(self, sc, dt):
        logger.debug("..:.. Creating instance of the FraudEngine class")
        # Spark Context and stream file path
        self.sc = sc
        
        # warehouse_location points to the default location for managed databases and tables
        self.warehouse_location = os.path.abspath('spark-warehouse')

        self.sqlc = SparkSession \
            .builder \
            .appName("ifds_server") \
            .config("spark.sql.warehouse.dir", warehouse_location) \
            .enableHiveSupport() \
            .getOrCreate()

        stream_data = sqlc.read.csv(dt, header = True, inferSchema = True)
        logger.debug("-- Retrieved data from data stream CSV")

        # Read data from database and put into a DF
        hist_data = self.sqlc.sql("SELECT * FROM hist_data")
        logger.debug("-- Retrieved data from Hive table")

        parsed_df = hist_data.drop(*['paysim_id', 'nameorig', 'namedest'])
        parsed_sd = stream_data.drop(*['paysim_id', 'nameorig', 'namedest'])
        
        # Convert type column
        indexer = StringIndexer(inputCol="type", outputCol="type_vec").fit(parsed_df)
        parsed_df = indexer.transform(parsed_df)
        parsed_sd = indexer.transform(parsed_sd)

        parsed_df = parsed_df.drop("type")
        parsed_sd = parsed_sd.drop("type")

        logger.debug("-- Finished StringIndexer from type column")

        # Vector Assembler
        ignore = ['isFraud']
        selectedCols = ['isFraud', 'features']

        ## Train
        assembler = VectorAssembler(
            inputCols=[x for x in parsed_df.columns if x not in ignore],
            outputCol='features'
        )

        final_df = assembler.transform(parsed_df)
        parsed_df = final_df.select(selectedCols)

        ## Test
        assembler = VectorAssembler(
            inputCols=[x for x in parsed_df.columns if x not in ignore],
            outputCol='features')

        final_df = assembler.transform(parsed_sd)
        self.parsed_sd = final_df.select(selectedCols)

        # Define and train the model
        self.model = self.__get_model(parsed_df)

        # Unpersist RDD
        hist_data.unpersist()
        parsed_df.unpersist()

    def __get_model(self, hRDD):
        logger.debug("--- Starting model training")

        # Train the model
        lr = LogisticRegression(
            featuresCol = 'features', 
            labelCol = 'label', 
            maxIter = 10
        )

        model = lr.fit(hRDD)
        return model

    def __process_stream(self, request):
        pass

    """
    @description: Retrieve simple statistics from stream table
    """
    def get_stats(self, window):
        pass

    """
    @description: 
    """
    def start_stream(self, window):
        pass

# Producer class to send the messages to Kafka broker
#class Producer(threading.Thread):
#    def __init__(self, data, time_window = 60.0, self.address = 'localhost:9092'):
#        # Hyper-parameters
#        self.data = data
#        self.topic = 'fraud_detection'
#
#        # Define Kafka producer to send Message through HTTP
#        self.producer = KafkaProducer(bootstrap_servers=self.address)
#    
#    def run(self):
#        n = self.data.shape[0]/self.time_window
#        for index, row in self.data.iterrows():
#            producer.send(self.topic, row.to_string())
#            time.sleep(n)
#
#        self.producer.close()