import logging

from flask import Blueprint, request, render_template, redirect, flash

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
    if db_session.query(FamilyMember).filter_by(name=name).first():
        flash("Sorry, user could not be added. That name is already being used by another family member", category='error')
        return

    link = request.form.get("link")
    caltype = request.form.get("calendarType")
    if link == "":
        link = None
    elif not is_valid_url(link, caltype):
        logging.warning("invalid url")
        return
    elif db_session.query(FamilyMember).filter_by(url=link).first():
        flash("Sorry, user could not be added. That calenader url is already being used by another family member", category='error')
        return

    if request.form.get("email") == "":
        email = None
    else:
        email = request.form.get("email")
    if email != None and db_session.query(FamilyMember).filter_by(email=email).first():
        flash("Sorry, user could not be added. That email is already being used by another family member", category='error')
        return

    icon = request.form.get("icon")
    eventsHash = 0
    userObject = User(name, link, caltype, email)
    row = FamilyMember(
        name=name,
        url=link,
        calendarType=caltype,
        email=email,
        icon=icon,
        eventsHash=eventsHash,
        userObject=userObject,
    )
    db_session.add(row)
    flash("Welcome to the family {}!".format(name), category='success')


def edit_family_member(db_session):
    originalName = request.form.get("personName")
    name = request.form.get("name")
    if (name != originalName and db_session.query(FamilyMember).filter(FamilyMember.name!=originalName).filter_by(name=name).first()):
        flash("Sorry, you can't update {}'s name to {}, another family member with that name already exists".format(originalName, name), category='error')
        return
    
    link = request.form.get("link")
    caltype = request.form.get("calendarType")
    if link == "":
        link = None
    elif (db_session.query(FamilyMember).filter(FamilyMember.name!=originalName).filter_by(url=link).first()):
        flash("Sorry that calendar url is already being used by another family member, could not update {}'s url".format(name), category='error')
        return
    
    if request.form.get("email") == "":
        email = None
    else:
        email = request.form.get("email")
    if email != None and (db_session.query(FamilyMember).filter(FamilyMember.name!=originalName).filter_by(email=email).first()):
        flash("Sorry, you cant update {}'s email to {}, it is already being used by another family member".format(name, email), category='error')
        return
    
    icon = request.form.get("icon")
    person = db_session.query(FamilyMember).get(originalName)
    userObject = User(name, link, caltype, email)
    
    if originalName != name:
        person.name = name
    if email != person.email:
        person.email = email
    if link != person.url:
        person.url = link
        person.calendarType = caltype
    if icon != person.icon:
        person.icon = icon
    person.userObject = userObject
    flash("{}'s information was successfully updated!".format(name), category='success')


def delete_family_member(db_session):
    name = request.form["submit"]
    person = db_session.query(FamilyMember).get(name)
    db_session.delete(person)
    flash("Successfully deleted {}".format(person.name), category='success')


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
