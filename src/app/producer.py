import time
import threading

import numpy as np
import pandas as pd

from kafka import KafkaProducer

# Producer class to send the messages to Kafka broker
class Producer(threading.Thread):
    def __init__(self, data, time_window = 60.0, self.address = 'localhost:9092'):
        # Hyper-parameters
        self.data = data
        self.topic = 'fraud_detection'

        # Define Kafka producer to send Message through HTTP
        self.producer = KafkaProducer(bootstrap_servers=self.address)
    
    def run(self):
        n = self.data.shape[0]/self.time_window
        for index, row in self.data.iterrows():
            producer.send(self.topic, row.to_string())
            time.sleep(n)

        self.producer.close()