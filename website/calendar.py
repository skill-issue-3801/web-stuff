import logging
import datetime

#     Above is for later, "{{ utc_dt }}" is the variable for date time in html
from flask import Blueprint, request, render_template

from .app import app


calendar = Blueprint("calendar", __name__)
logger = logging.getLogger(__name__)


@calendar.route("/", methods=["GET"])
def default():
    return render_template("calendar.html")
