import logging

from flask import Blueprint, request, render_template

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

# Connects to the Calendar set up page (config)
@admin.route("/add_calendars", methods=["GET", "POST"])
def add_calendars():
    if request.method == "GET":
        return render_template('calendarSetUp.html')

    db_session = app.db_session()
    db_session.add(CalendarLocations(name="NAME", url="URL"))
    db_session.commit()
    db_session.close()


@admin.route("/my_family", methods=["GET", "POST"])
def my_family():
    if request.method == "GET":
        return render_template('family.html')

# Connects to the Guide page
@admin.route("/help", methods=["GET"])
def help():
    return render_template('guide.html')


@admin.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "GET":
        return render_template('settings.html')