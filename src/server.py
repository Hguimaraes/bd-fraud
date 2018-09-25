#!/usr/bin/env python
import argparse
import os
import sys
import time
import cherrypy
from paste.translogger import TransLogger

from app import create_app
from pyspark import SparkContext, SparkConf
 
def init_spark_context():
    # load spark context
    conf = SparkConf().setAppName("ifds_server")

    # Defining Spark Context
    sc = SparkContext(conf = conf, pyFiles=['engine.py', 'app.py'])

    return sc
 
 
def run_server(app, port):
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)
 
    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')
 
    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': port,
        'server.socket_host': '0.0.0.0'
    })
 
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
 
 
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fraud detection system using Big Data Technologies')

    # Required argument
    parser.add_argument('-p', '--port', help='Port to deploy the solution', type=str, required=True)
    parser.add_argument('-d', '--data', help='Path to dataset in CSV format to stream to the solution',
        type=str, required=True)
    args = parser.parse_args()

    # Pass args, activate logging and start the main function
    args = parser.parse_args()

    # Init spark context and load libraries
    sc = init_spark_context()
    app = create_app(sc, args.data)
 
    # start web server
    run_server(app, args.port)