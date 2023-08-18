import os
import logging

import waitress

from .app import app

def main(args):
    logging.basicConfig(level=logging.INFO);
    
    app.config["SERVER_NAME"] = os.environ.get("APP_BASE_URL")
    waitress.serve(app, host=args[1], port=9003)

    logging.info("Website is up and awaiting requests.")
