import time
import numpy as np
import pandas as pd

from .engine import Engine

# Retrieve the Singleton
engine = Engine()

def start_stream():
    # Read the CSV file for streaming
    try:
        df = pd.read_csv(engine.args.data)
    except IOError:
        print('File not found! Start stream failed.')
        raise
    

def get_stats():
    pass