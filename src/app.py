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
    #logger.debug("User %s TOP ratings requested", user_id)
    #top_ratings = recommendation_engine.get_top_ratings(user_id,count)
    #return json.dumps(top_ratings)
    pass
 
@main.route("/stream/<int:time_window>", methods=["GET"])
def start_stream(time_window):
    #logger.debug("User %s rating requested for movie %s", user_id, movie_id)
    #ratings = recommendation_engine.get_ratings_for_movie_ids(user_id, [movie_id])
    #return json.dumps(ratings)
    pass
 
def create_app(sc, stream_path):
    #global recommendation_engine 
    #recommendation_engine = RecommendationEngine(sc, stream_path)    
    
    #app = Flask(__name__)
    #app.register_blueprint(main)
    #return app
    pass