from flask import Flask
from .engine import Engine
#from pyspark import SparkContext
#from pyspark.sql import SQLContext

# Flask application
def start(args):
    # Start the big data project for Fraud Detection
    Engine(args).start()

app = Flask(__name__, static_folder = '../static/')
from app import routes

# Spark dependencies
#sc = SparkContext()
#sqlc = SQLContext(sc)