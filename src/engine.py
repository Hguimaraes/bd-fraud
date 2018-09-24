import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
"""
class FraudEngine:
    """
    """
    def __init__(self, sc, dt = ""):
        # Spark Context
        self.sc = sc

        # Read data from database and put into a RDD
        hist_data = None

        # Define and train the model
        self.model, self.train_stats = self.__get_model(hist_data)

        # Unpersist RDD
        hist_data.unpersist()

    def __get_model(self, hRDD):
        pass

    def __process_stream(self, request):
        pass

    def __save_to_database(self, hRDD):
        pass

    """
    @description: Retrieve simple statistics from stream table
    """
    def get_stats(self):
        pass
