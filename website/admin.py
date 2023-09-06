import logging

from flask import Blueprint, request, render_template, redirect

from .models import CalendarLocations
from .base import has_db


admin = Blueprint("admin", __name__)
logger = logging.getLogger(__name__)


@admin.route("/", methods=["GET"])
def default():
    return """<p>This is the admin page.<br>
<a href="/admin/add_calendars">Add calendars.</a><br>
<a href="/admin/manage_family">Change family settings.</a><br>
<a href="/admin/help">Get help.</a><br>
<a href="/admin/settings">Advanced settings.</a></p>"""


# Connects to the Calendar set up page (config)
@admin.route("/add_calendars", methods=["GET"])
def add_calendars():
    return render_template("calendarSetUp.html")


@admin.route("/add_calendars", methods=["POST"])
@has_db
def calendars_post(db_session):
    db_session.add(CalendarLocations(family_member_name="NAME", url="URL"))
    db_session.commit()
    db_session.close()

    return add_calendars()


@admin.route("/manage_family", methods=["GET"])
def manage_family():
    return render_template("manageFamily.html")


@admin.route("/manage_family", methods=["POST"])
@has_db
def family_post(db_session):
    db_session.add()
    db_session.commit()
    db_session.close()

    return manage_family()


# Connects to the Guide page
@admin.route("/help", methods=["GET"])
def help():
    return render_template("guide.html")


@admin.route("/customise", methods=["GET"])
def customise():
    return render_template("customise.html")


@admin.route("/customise", methods=["POST"])
@has_db
def customise_post(db_session):
    db_session.add()
    db_session.commit()
    db_session.close()

    return customise()
