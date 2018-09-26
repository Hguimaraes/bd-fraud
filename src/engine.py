import os
import time
import logging
import threading
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.clustering import KMeans

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
@description: Class to abstract all Spark computations
"""
class FraudEngine:
    def __init__(self, sc, dt):
        logger.debug("..:.. Creating instance of the FraudEngine class")
        # Init stream init
        self.stream_state = False
        self.stream_stats = {'fraud': 0, 'legit': 0}

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
        # Apply strauss method for balancing the data
        df = self.__strauss(df)

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

    def __process_stream(self, window):
        # Block new requests
        self.stream_state = True

        # @TODO: Implement a method to stream self.st_data in a window of time
        # Test and return statistics
        predictions = rfmodel.transform(self.st_data)
        self.stream_stats = {'fraud': 0, 'legit': 0}
        
        # Receive new requests
        self.stream_state = False
        
        return None

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

    def __strauss(self, df, k = 7):
        # Separe the dataset by labels
        f_df = df.filter(df.label == 1.0)
        nf_df = df.filter(df.label == 0.0)

        # Trains a k-means model.
        kmeans = KMeans().setK(k).setSeed(1)
        model = kmeans.fit(nf_df)

        # Evaluate clustering by computing Within Set Sum of Squared Errors.
        wssse = model.computeCost(nf_df)
        logger.debug("Within Set Sum of Squared Errors = {}".format(wssse))

        # Balanced the data with strauss method
        cls = model.transform(nf_df)

        d = {}
        n_list = []
        for c in range(k):
            df_temp = cls.filter(cls.prediction == c)
            n_temp = df_temp.count()
            
            n_sample = (n_temp*(0.25)*(2.17**2))/(0.25*(2.17**2)+(n_temp -1)*(0.02**2))
            ratio = n_sample/n_temp
            d[c] = df_temp.sample(False, ratio)
        
        new_df = d[0]
        for i in range(1,k):
            new_df = new_df.union(d[i])
        new_df = new_df.drop("prediction")
        new_df = new_df.union(f_df)
        
        # Return the new training set
        return new_df

    """
    @description: Retrieve simple statistics from stream table
    """
    def get_stats(self):
        return self.stream_stats

    """
    @description: Return train statistics
    """
    def get_train_stats(self):
        return {'AUC': self.train_stats}

    """
    @description: @TODO: Implement a stream process
    """
    def start_stream(self, window):
        msg = "A stream de dados teste já foi iniciada, aguarde!"
        if not self.stream_state:
            msg = "Iniciando processo de streaming!"
            self.__process_stream(window)
        return {'msg': msg}