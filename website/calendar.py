import logging
import pytz
from .cal import *
from datetime import datetime
from .base import has_global_stuff, has_db
from .models import FamilyMember

#     Above is for later, "{{ utc_dt }}" is the variable for date time in html
from flask import Blueprint, request, render_template

from .app import app


calendar = Blueprint("calendar", __name__)
logger = logging.getLogger(__name__)


@calendar.route("/", methods=["GET"])
@has_global_stuff
def default(db_session, globals):
    if not __debug__:
        return "Raspberry Pi access only.", 403

    family = db_session.query(FamilyMember).all()
    anyChanges = False
    today = datetime.utcnow().replace(tzinfo=pytz.utc).date()
    hashes = {}
    for member in family:
        newHash = check_cal_for_updates(
            member.url, member.calendarType, member.eventsHash, today
        )
        if newHash == False:
            hashes[member.name] = member.eventsHash
        else:
            hashes[member.name] = newHash
            anyChanges = True
    if anyChanges or globals.familyChanges:
        # unpickle
        userObjects = {}
        for member in family:
            userObjects[member.name] = member.userObject
        evs = do_update(userObjects.values(), today, hashes)
        for member in family:
            member.eventsHash = hashes[member.name]
            member.userObject = userObjects[member.name]
        globals.set_events(calendarise_events(evs))
    db_session.commit()
    globals.familyChanges = False
    anyChanges = False
    log_events(globals.events)
    familyMembers = {}
    for person in family:
        familyMembers[person.name] = person
    return render_template("calendar.html", events=globals.events, family=familyMembers)


def do_update(userObjects, today, hashes):
    logging.warning("doing update")
    names = []
    emails = []
    for user in userObjects:
        names.append(user.get_name())
        if user.get_email() != None:
            emails.append(user.get_email())
    return update_events(userObjects, today, hashes, names, emails)


def log_events(events):
    logging.warning("Events:")
    for event in events:
        logging.warning(
            "{} {} {} {}".format(
                event.summary, event.start, event.uid, str(event.attendees)
            )
        )


@calendar.route("/do_update", methods=["POST"])
@has_global_stuff
def update(db_session, globals):
    family = db_session.query(FamilyMember).all()
    anyChanges = False
    today = datetime.utcnow().replace(tzinfo=pytz.utc).date()
    hashes = {}
    check_for_update(family, anyChanges, today, hashes)

    if anyChanges or globals.familyChanges:
        jsonfile = do_update(family, today, hashes)
        return jsonfile
    else:
        return json.dumps(globals.events)
