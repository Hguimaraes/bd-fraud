from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
from engine import FraudEngine
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request

@main.route("/train_stats/", methods=["GET"])
def get_train_stats():
    logger.debug("Retrieving statistics from training phase")
    stats = fraud_engine.get_train_stats()
    return json.dumps(stats), 200
 
@main.route("/stats/", methods=["GET"])
def get_stats():
    logger.debug("Retrieving statistics for the new request")
    stats = fraud_engine.get_stats()
    return json.dumps(stats), 200
 
@main.route("/stream/<int:time_window>", methods=["GET"])
def start_stream(time_window):
    logger.debug("Starting stream requested. Using a time window of %s seconds.", time_window)
    msg = fraud_engine.start_stream(time_window)
    return json.dumps(msg), 200
 
def create_app(sc, stream_path):
    global fraud_engine 
    fraud_engine = FraudEngine(sc, stream_path)
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app