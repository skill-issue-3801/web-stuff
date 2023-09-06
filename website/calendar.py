import logging
import datetime
from .base import has_global_stuff, has_db

#     Above is for later, "{{ utc_dt }}" is the variable for date time in html
from flask import Blueprint, request, render_template

from .app import app


calendar = Blueprint("calendar", __name__)
logger = logging.getLogger(__name__)


@calendar.route("/", methods=["GET"])
def default():
    return render_template("calendar.html")

@calendar.route("/do_update")
@has_global_stuff
@has_db
def update(session, global_state):
    global_state.set_events(global_state.events + ["xyz"])
    return str(global_state.events)