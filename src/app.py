from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
from engine import FraudEngine
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request
 
@main.route("/stats/<int:time_window>", methods=["GET"])
def get_stats(time_window):
    logger.debug("Statistics from the last %s seconds requested", time_window)
    stats = fraud_engine.get_stats(time_window)
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