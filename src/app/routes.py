from app import app
from .engine import Engine
from .process import start_stream
from .process import get_stats

# Retrieve the Singleton
engine = Engine()

"""
@Description: Main page of the app
"""
@app.route('/')
def root():
    return app.send_static_file('index.html')

"""
@description: Method to start the Producer to stream data into the app
"""
@app.route('/stream')
def stream():
    start_stream()
    return 200

"""
@description: Method to return the current statistics of the app
"""
@app.route('/stats')
def stats():
    stats = get_stats()
    return stats, 200