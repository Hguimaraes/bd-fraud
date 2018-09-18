#!/usr/bin/env python
import sys
import argparse
from app import app, start


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fraud detection system using Big Data Technologies')

    # Required argument
    parser.add_argument('-p', '--port', help='Port to deploy the solution', type=str, required=True)
    parser.add_argument('-d', '--data', help='Data in CSV format to stream to the solution', type=str, required=True)
    args = parser.parse_args()

    # Pass args, activate logging and start the main function
    args = parser.parse_args()

    # Start the main application and start the web server
    start(args)
    app.run(port = int(args.port), threaded = True, debug = True)