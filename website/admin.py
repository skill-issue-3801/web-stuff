import logging

from flask import Blueprint

from .models import CalendarLocations
from .app import app

admin = Blueprint("admin", __name__)
logger = logging.getLogger(__name__)


@admin.route("/", methods=["GET"])
def default():
    return """<p>This is the admin page.<br>
<a href="/admin/add_calendars">Add calendars.</a><br>
<a href="/admin/my_family">Change family settings.</a><br>
<a href="/admin/help">Get help.</a><br>
<a href="/admin/settings">Advanced settings.</a></p>"""


@admin.route("/add_calendars", methods=["GET", "POST"])
def add_calendars():
    if request.method == "GET":
        return "<p>This is the page to add calendars.</p>"

    db_session = app.db_session()
    db_session.add(CalendarLocations(name="NAME", url="URL"))
    db_session.commit()
    db_session.close()

@admin.route("/my_family", methods=["GET", "POST"])
def my_family():
    if request.method == "GET":
        return "<p>This is the page for user settings.</p>"

@admin.route("/help", methods=["GET"])
def help():
    return "<p>This is the help page.</p>"

@admin.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "GET":
        return """<p>This is the page for advanced/display settings.<br>
                  e.g. link tags to accounts, change colours, dark/light mode</p>"""
