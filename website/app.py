from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker

from .models import CalendarLocations


class DecoWebsite(Flask):
    def set_db_engine(self, db_engine):
        self.db_session = sessionmaker(bind=db_engine)

    def send_static_file(self, filename: str, subdomain=None):
        return super(DecoWebsite, self).send_static_file(filename)


app = DecoWebsite(__name__, static_folder=None)


@app.route("/")
def home():
    return render_template('calendar-attempt-1.html')
# web-stuff\website\Front-end\calendar-attempt-1.html

# def hello_world():
#     return """ <link rel="stylesheet" href="url_for('static', filename='/Front-end/css/main.css'">
#     <p> The website for deco3801 2023 team 'skill issue'. Check out <a href="/admin">the admin page</a>.
#     </p>"""
