import logging

from sqlalchemy import create_engine
from .models import Base
import waitress

from .app import app
from .admin import admin
from .calendar import calendar


def main(db_url, args):
    logging.basicConfig(level=logging.INFO)

    # app.config["SERVER_NAME"] = os.environ.get("APP_BASE_URL")

    db_engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(db_engine)
    app.set_db_engine(db_engine)

    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(calendar, url_prefix="/calendar")

    waitress.serve(app, host=args[1], port=9003)

    logging.info("Website is up and awaiting requests.")
