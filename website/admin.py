import logging

from flask import Blueprint, request, render_template, redirect

from .cal import User, is_valid_url
from .models import FamilyMember
from .base import has_db, has_global_stuff


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
    db_session.add(
        FamilyMember(
            name="NAME", url="URL", calendarType="apple", eventsHash=0, userObject=None
        )
    )
    db_session.commit()
    db_session.close()

    return add_calendars()


@admin.route("/manage_family", methods=["GET"])
@has_db
def manage_family(db_session):
    family = db_session.query(FamilyMember).all()
    db_session.close()
    return render_template("manageFamily.html", family=family)


@admin.route("/manage_family", methods=["POST"])
@has_global_stuff
def family_post(db_session, globals):
    if request.form.get("formName") == "addFamilyMember":
        add_family_member(db_session)
        globals.familyChanges = True
    elif request.form.get("formName") == "editFamilyMember":
        edit_family_member(db_session)
        globals.familyChanges = True
    elif request.form.get("formName") == "deleteFamilyMember":
        delete_family_member(db_session)
        globals.familyChanges = True
    db_session.commit()
    db_session.close()
    return redirect("/admin/manage_family")


def add_family_member(db_session):
    name = request.form.get("name")

    link = request.form.get("link")
    caltype = request.form.get("calendarType")
    if not is_valid_url(link, caltype):
        logging.warning("invalid url")
        return
    if request.form.get("email") == "":
        email = None
    else:
        email = request.form.get("email")
    if db_session.query(FamilyMember).filter_by(name=name).first():
        logging.warning("that name is already being used")
        return
    if db_session.query(FamilyMember).filter_by(url=link).first():
        logging.warning("that url is already being used")
        return
    if email != None and db_session.query(FamilyMember).filter_by(email=email).first():
        logging.warning("that email is already being used")
        return
    icon = "/graphics/fish.png"
    eventsHash = 0
    userObject = User(name, link, caltype, email)
    column = FamilyMember(
        name=name,
        url=link,
        calendarType=caltype,
        email=email,
        icon=icon,
        eventsHash=eventsHash,
        userObject=userObject,
    )
    db_session.add(column)


def edit_family_member(db_session):
    logging.warning("i dont know how to do this yet")


def delete_family_member(db_session):
    name = request.form["submit"]
    person = db_session.query(FamilyMember).get(name)
    db_session.delete(person)


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
