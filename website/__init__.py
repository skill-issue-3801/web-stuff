import logging

import sqlalchemy
import waitress

from .app import app
from .admin import admin
from .calendar import calendar
from .base import Session, DB
from .models import Base


def main(db_url, args):
    logging.basicConfig(level=logging.INFO)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    with app.app_context():
        s = Session()
        Base.metadata.create_all(s.connection())
        s.commit()

    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(calendar, url_prefix="/calendar")

    waitress.serve(app, host=args[1], port=9003)

    logging.info("Website is up and awaiting requests.")
