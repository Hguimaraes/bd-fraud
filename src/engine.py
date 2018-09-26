import os
import time
import logging
import threading
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.mllib.linalg import DenseVector
from pyspark.mllib.regression import LabeledPoint
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator

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
            .config("spark.sql.warehouse.dir", self.warehouse_location) \
            .enableHiveSupport() \
            .getOrCreate()

        stream_data = self.sqlc.read.csv(dt, header = True, inferSchema = True)
        logger.debug("-- Retrieved data from data stream CSV")

        # Read data from database and put into a DF
        hist_data = self.sqlc.sql("SELECT * FROM hist_data")
        logger.debug("-- Retrieved data from Hive table")

        # Process the input dataframe
        parsed_df = self.__clean_data(hist_data)
        self.st_data = self.__clean_data(stream_data, is_fraud = "isFraud")
        
        # Define and train the model
        self.model, self.train_stats = self.__get_model(parsed_df)

        # Unpersist RDD
        hist_data.unpersist()
        parsed_df.unpersist()

    def __get_model(self, df):
        logger.debug("--- Starting model training")
        train, test = df.randomSplit([0.7, 0.3], seed = 2018)

        # Train a random forest model
        rf = RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=10)
        rfmodel= rf.fit(train)
        
        # Test and return statistics
        evaluator = BinaryClassificationEvaluator()
        predictions = rfmodel.transform(test)
        stats = evaluator.evaluate(predictions)

        return rfmodel, stats

    def __process_stream(self, request):
        pass

    def __clean_data(self, df, is_fraud = "isfraud"):
        ignore = [is_fraud,'label']

        #Removendo colunas não utilizadas
        df = df.drop(*['paysim_id', 'nameorig', 'namedest'])

        #String Indexing
        string_indexer = StringIndexer(inputCol="type", outputCol="type_numeric").fit(df)
        df = string_indexer.transform(df)
        df = df.drop(df.type)

        #One-hot encoding
        encoder = OneHotEncoder(inputCol="type_numeric", outputCol="type_vector")
        df = encoder.transform(df)
        df = df.drop("type_numeric")

        #Label encoding
        label_stringIdx = StringIndexer(inputCol = is_fraud, outputCol = 'label').fit(df)
        df = label_stringIdx.transform(df)
        df = df.drop(is_fraud)

        #Vector Assembling
        assembler = VectorAssembler(
            inputCols=[x for x in df.columns if x not in ignore],
            outputCol='features')
        df = assembler.transform(df)

        # dataframe in the correct format
        selectedCols = ['label', 'features']
        df = df.select(selectedCols)

        return df

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