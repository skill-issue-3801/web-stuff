from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker

from .models import CalendarLocations


class DecoWebsite(Flask):
    def set_db_engine(self, db_engine):
        self.db_session = sessionmaker(bind=db_engine)


# In theory what static_folder="templates" does is whenever app
# looks for a static folder it looks under templates
app = DecoWebsite(__name__, static_folder="templates")


@app.route("/")
def home():
    return render_template("index.html")
