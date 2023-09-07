import logging

from flask import Blueprint, request, render_template, redirect

from .cal import User
from .models import FamilyMember
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
    db_session.add(FamilyMember(name="NAME", url="URL", calendarType="apple", eventsHash=0, userObject=None))
    db_session.commit()
    db_session.close()

    return add_calendars()


@admin.route("/manage_family", methods=["GET"])
@has_db
def manage_family(db_session):
    logging.warning("")
    logging.warning("!!! Get")
    results = db_session.query(FamilyMember).all()
    for res in results:
        logging.warning(res.name)
    return render_template("manageFamily.html")


@admin.route("/manage_family", methods=["POST"])
@has_db
def family_post(db_session):
    logging.warning("")
    logging.warning("!!! Post")
    if (request.form.get('formName') == "addFamilyMember"):
        add_family_member(db_session)
    elif (request.form.get('formName') == "editFamilyMember"):
        edit_family_member(db_session)
    return redirect("/admin/manage_family")

def add_family_member(db_session):
    name = request.form.get('name')
    link = request.form.get('link')
    caltype = request.form.get('calendarType')
    if request.form.get('email') == '':
        email = None
    else:
        email = request.form.get('email')
    icon = "icons/fish.jpeg" 
    eventsHash = 0
    userObject = User(name, link, caltype, email)
    column = FamilyMember(name=name, url=link, calendarType=caltype, email=email, icon=icon, eventsHash=eventsHash, userObject=userObject)
    db_session.add(column)
    db_session.commit()

def edit_family_member(db_session):
    name = request.form.get('name')
    link = request.form.get('link')
    caltype = request.form.get('calendarType')
    if request.form.get('email') == '':
        email = None
    else:
        email = request.form.get('email')
    icon = "icons/fish.jpeg" 
    eventsHash = 0
    userObject = User(name, link, caltype, email)
    # not done yet
    #column = FamilyMember(name=name, url=link, calendarType=caltype, email=email, icon=icon, eventsHash=eventsHash, userObject=userObject)
    #db_session.add(column)
    db_session.commit()

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
