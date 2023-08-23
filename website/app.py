from flask import Flask
from sqlalchemy.orm import sessionmaker

from .models import CalendarLocations 

class DecoWebsite(Flask):
    def set_db_engine(self, db_engine):
        self.db_session = sessionmaker(bind = db_engine)


app = DecoWebsite(__name__, static_folder=None)


@app.route("/")
def hello_world():
    db_session = app.db_session()
    query = db_session.query(CalendarLocations)

    return f"<p>Hello, World!</p>\n{query}"
