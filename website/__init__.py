import os
import logging

import waitress
from flask import Flask


def main(args):
    logging.basicConfig(level=logging.INFO);
    
    app = Flask(__name__, static_folder=None);
    app.config["SERVER_NAME"] = os.environ.get("APP_BASE_URL")
    waitress.serve(app, host=args[1], port=9003)

    logging.info("Website is up and awaiting requests.")
