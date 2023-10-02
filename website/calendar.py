import logging
import math
import pytz
import json
from .cal import *
from datetime import datetime
from .base import has_global_stuff
from .models import FamilyMember

#     Above is for later, "{{ utc_dt }}" is the variable for date time in html
from flask import Blueprint, render_template

from .app import app


calendar = Blueprint("calendar", __name__)
logger = logging.getLogger(__name__)


@calendar.route("/", methods=["GET"])
@has_global_stuff
def default(db_session, globals):
    if not __debug__:
        return "Raspberry Pi access only.", 403

    family = db_session.query(FamilyMember).all()
    today = datetime.utcnow().replace(tzinfo=pytz.utc).date()
    hashes = {}
    anyChanges = check_for_update(family, today, hashes)
    if anyChanges or globals.familyChanges:
        jsonfile = do_update(family, today, hashes)
        globals.set_events(json.loads(jsonfile))
        db_session.commit()

    globals.familyChanges = False
    anyChanges = False
    log_events(globals.events)
    familyMembers = {}
    for person in family:
        familyMembers[person.name] = person
    firstDay = today - timedelta(days=((today.weekday() + 1) % 7))
    dates = []
    for i in range(0, 7):
        dates.append((firstDay + timedelta(days=i)).strftime("%d"))
    return render_template(
        "calendar.html",
        events=globals.events,
        datesArray = dates_array(firstDay),
        numWeeks = total_weeks_loaded,
        thisWeekIndex = math.floor(total_weeks_loaded /2),
        family=familyMembers,
        todayIndex=(today.weekday() + 1) % 7,
        firstDay = firstDay,
        uids=uids_to_div_dict(family)
    )


def uids_to_div_dict(family):
    peoplesUid = {}
    for member in family:
        peoplesUid[member.name] = member.userObject.get_uids()
    return peoplesUid


def check_for_update(family, today, hashes):
    anyChanges = False
    for member in family:
        if member.url != None:
            newHash = check_cal_for_updates(
                member.url, member.calendarType, member.eventsHash, today
            )
            if newHash == False:
                hashes[member.name] = member.eventsHash
            else:
                hashes[member.name] = newHash
                anyChanges = True
        else:
            hashes[member.name] = member.eventsHash
    return anyChanges


def do_update(family, today, hashes):
    userObjects = {}
    for member in family:
        userObjects[member.name] = member.userObject
    names = []
    emails = []
    for user in userObjects.values():
        names.append(user.get_name())
        if user.get_email() != None:
            emails.append(user.get_email())
    evs = update_events(userObjects.values(), today, hashes, names, emails)
    for member in family:
        member.eventsHash = hashes[member.name]
        member.userObject = userObjects[member.name]
    return json.dumps(calendarise_events(evs, family, today))

def log_events(events):
    logging.warning("Events:")
    for week in events:
        for event in week:
            logging.warning(
                "{} {} {} {}".format(
                    event["summary"], event["start"], event["uid"], str(event["attendees"])
                )
            )
        logging.warning("...")


@calendar.route("/do_update", methods=["POST"])
@has_global_stuff
def update(db_session, globals):
    family = db_session.query(FamilyMember).all()
    today = datetime.utcnow().replace(tzinfo=pytz.utc).date()
    hashes = {}
    anyChanges = check_for_update(family, today, hashes)

    if anyChanges or globals.familyChanges:
        jsonfile = do_update(family, today, hashes)
        return jsonfile
    else:
        return json.dumps(globals.events)
