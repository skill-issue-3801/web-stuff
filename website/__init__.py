import os
import logging

import waitress

from .app import app


def main(db_url, args):
    logging.basicConfig(level=logging.INFO)

    app.config["SERVER_NAME"] = os.environ.get("APP_BASE_URL")

    db_engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(db_engine)
    app.set_db_engine(db_engine)

    waitress.serve(app, host=args[1], port=9003)

    logging.info("Website is up and awaiting requests.")
