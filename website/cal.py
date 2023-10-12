import json
import math
import validators
from datetime import timedelta, datetime
from icalevents import icalevents, icalparser

accepted_calendars = ["google", "apple", "none"]
weekdays = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
}
load_past_weeks = 5
load_future_weeks = 5
total_weeks_loaded = load_past_weeks + load_future_weeks + 1

class User:
    """An object representing a user/family member
    Attributes:
        _name (string): This user's name, this is a unique identifier
        _calendar_link (string): The url for this user's calendar
        _caltype (string): either 'google or 'apple' depending of the calendar platfrom
            this user's link is from
        _email (string): this user's email address
        _event_list (list of icalevents.icalevents.Event): the events from this user's
            calendar that will be placed on the family calendar
        _events_hash (int) the hash of this user's events, used to check if there has
            been any changes
        _my_event_uids (list of str): the unique id of all events thsi user is attending
    """

    def __init__(self, name, calendar_link, caltype, email):
        self._name = name

        self._calendar_link = calendar_link
        if calendar_link == None:
            self._caltype = "none"
        else:
            self._caltype = caltype

        if email != None:
            self._email = "mailto:" + email
        else:
            self._email = None

        self._event_list = []
        self._events_hash = -1
        self._my_event_uids = []

    def get_name(self):
        return self._name

    def set_name(self, newname):
        self._name = newname

    def get_link(self):
        return self._calendar_link

    def get_caltype(self):
        return self._caltype

    def set_link(self, calendar_link, caltype):
        self._calendar_link = calendar_link
        self._caltype = caltype

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = "mailto:" + email

    def get_events(self):
        return self._event_list

    def get_hash(self):
        return self._events_hash

    def set_hash(self, evshash):
        self._events_hash = evshash

    def set_events(self, event_list):
        self._event_list = event_list

    def clear_uids(self):
        self._my_event_uids = []

    def get_uids(self):
        return self._my_event_uids

    def set_uids(self, uids):
        self._my_event_uids = uids


def is_valid_url(url, caltype):
    if (
        caltype == "google"
        and validators.url(url.strip())
        and url[0:42] == "https://calendar.google.com/calendar/ical/"
        and url[-10:] == "/basic.ics"
    ):
        return True
    elif (
        caltype == "apple" and url[0:42] == "webcal://p122-caldav.icloud.com/published/"
    ):
        return True
    else:
        return False


def events_get_hash(events):
    hashstr = ""
    for event in events:
        hashstr += str(event)
        hashstr += str(event.description)
    return hash(hashstr)


def update_user_email(names, emails, name, newEmail, user):
    if not name in names:
        print("There is no user by the name ", name, "to edit")
        return False

    if newEmail in emails:
        print("Sorry, a user is already associated with this email: ", newEmail)
        return False

    if not validators.email(newEmail.strip()):
        print("Sorry,", newEmail, " is an invalid email")
        return False

    user.set_email(newEmail.strip())
    return True


def update_user_cal_link(names, urls, name, newLink, caltype, user):
    if not name in names:
        print("There is no user by the name ", name, "to edit")
        return False

    if newLink in urls:
        print("Sorry, a user is already using that calendar link")
        return False

    if caltype in accepted_calendars:
        user.set_link(newLink, caltype)
        return True
    else:
        print(
            "Sorry, ",
            caltype,
            " is not an accepted calendar type, must be 'apple', 'google', or 'none'",
        )
        return False


# I AM CONSIDERING SCRAPPING THIS FOR SIMPLICITY, IF THEY REALLY WANT TO THEY CAN JUST DELETE AND MAKE A NEW USER
def update_user_name(names, name, newName, user):
    if not name in names:
        print("There is no user by the name ", name, "to edit")
        return False

    if newName in names:
        print(
            "There is another user already using the name",
            newName,
            ", names must be unique",
        )
        return False

    user.set_name(newName)
    print(
        "Warning: events where",
        newName,
        "was invited by tagging them in the description"
        " using their old name will not appear unless you update them in your calendar!",
    )
    return True


def time_frame_to_download(today):
    day = (today.weekday() + 1) % 7
    start = today - timedelta(days=day, weeks = load_past_weeks)
    end = today + timedelta(days=6-day, weeks = load_future_weeks)
    return (start, end)


def check_cal_for_updates(url, caltype, hash, today):
    start, end = time_frame_to_download(today)
    if url == None:
        return False
    evs = icalevents.events(
        url=url, start=start, end=end, sort=True, fix_apple=(caltype == "apple")
    )
    evshash = events_get_hash(evs)
    if evshash == hash:
        return False  # no update needed
    return evshash  # this user has some changes to apply


def update_events(family, today, hashes, names, emails):
    return_events = []
    for member in family:
        if member.get_link() == None:
            # they dont have their own calendar, all their events will be added via other people
            continue
        elif hashes[member.get_name()] == member.get_hash():
            # their events have not changed, we will still check if they attend anything though
            return_events.extend(member.get_events())
        else:
            # their events have changed somehow, reprocess
            member.set_hash(
                hashes[member.get_name()]
            )  # record hash of events before processing
            start, end = time_frame_to_download(today)
            evs = icalevents.events(
                url=member.get_link(),
                start=start,
                end=end,
                sort=True,
                fix_apple=(member.get_caltype() == "apple"),
            )
            for event in evs:
                if process_attendees(member.get_name(), event, family, names, emails):
                    return_events.append(event)
            member.set_events(evs)
    fill_uids(family, return_events)
    return return_events


def fill_uids(family, events):
    newUids = {}
    for member in family:
        member.clear_uids()
        newUids[member.get_name()] = []
    for event in events:
        for attendee in event.attendee:
            newUids[attendee].append(event.uid)
    for member in family:
        member.set_uids(newUids[member.get_name()])


def process_attendees(calowner, event, family, names, emails):
    """Process the detected attendees and anyone named in the first line of the
        description, and add their name to the event.attendee list

    Args:
        calowner (string): The name if the user who owns the calendar this event was found on
        event (icalevents.icalevents.Event): The event to parse
        family (Family): The family of the calendar owner

    Returns:
        Bool: Return True if this event should be added to the family calender (if either
           cal owner or someone outside the family organised this event). Return False
           otherwise (if this event was organised someone else in the family it will be
           added from their calendar instead).
    """
    cpy_att = event.attendee
    event.attendee = set()
    # if people were added through calendar serviec invites, add them here
    if event.organizer != None:  # has invitees, add them before adding from description
        if event.organizer == None:  # no attendees added
            org_name = calowner
        elif (
            event.organizer in emails
        ):  # attendees addded and was made by someone in family
            org_name = get_email_owner(event.organizer, family)
        else:  # attendees added and organised by someone outside family, give this event to calowner
            org_name = calowner

        if org_name == calowner:  # event organised by the owner of this calendar
            event.attendee.add(calowner)  # add organiser
            if type(cpy_att) == list:
                # if there are many attendees, add all
                for att in cpy_att:
                    user_name = get_email_owner(att, family)
                    if user_name != None:  # if this email belongs to a family member
                        event.attendee.add(user_name)
            elif type(cpy_att) == icalparser.Attendee:
                # if there is 1 attendee
                user_name = get_email_owner(att, family)
                if user_name != None:  # add them if they are family
                    event.attendee.add(user_name)
        else:  # event organised by another family member, we will append form their calendar
            return False

    # if people were added in description, add them here
    if event.description != None:
        attendees = ((event.description).splitlines()[0]).split(",")
        for person in attendees:
            if person.strip() in names:
                event.attendee.add(person.strip())
    return True


def get_email_owner(email, family):
    for member in family:
        if member.get_email() == email:
            return member.get_name()
    return None

def get_weeks_index(day, firstSunday):
    thisWeekStart = day - timedelta(days=((day.weekday() + 1) % 7))
    return (int((thisWeekStart - firstSunday).days / 7))
    
def calendarise_events(events, family, today):
    familyMembers = {}
    for person in family:
        familyMembers[person.name] = person
    
    parsedEvents = [[] for _ in range(total_weeks_loaded)]
    firstSunday = today - timedelta(days=((today.weekday() + 1) % 7), weeks=load_past_weeks)
    
    for event in events:
        manstart = event.start
        while manstart.date() <= event.end.date():
            if (manstart.date() == event.end.date()) or (
                event.end
                == ((event.start + timedelta(days=1)).replace(hour=00, minute=00))
            ):
                parsedEvents[get_weeks_index(manstart.date(), firstSunday)].append(
                    htmlEvent(
                        event.summary,
                        event.uid,
                        event.attendee,
                        familyMembers,
                        event.start,
                        event.end,
                        manstart,
                        event.end,
                    )
                )
                break
            else:
                manualEnd = (event.start).replace(hour=00, minute=00)
                parsedEvents[get_weeks_index(manstart.date(), firstSunday)].append(
                    htmlEvent(
                        event.summary,
                        event.uid,
                        event.attendee,
                        familyMembers,
                        event.start,
                        event.end,
                        manstart,
                        manualEnd,
                    )
                )
                manstart = (event.start + timedelta(days=1)).replace(hour=00, minute=1)
    return parsedEvents

class htmlEvent(dict):
    def __init__(self, summary, uid, attendees, family, start, end, gridStart, gridEnd):
        dict.__init__(
            self,
            summary=summary,
            uid=uid,
            attendees=[{"name": a, "icon": family[a].icon} for a in attendees],
            start=str(start.strftime("%I:%M %p")),
            end=str(end.strftime("%I:%M %p")),
            colstart=gridStart.strftime("%A"),
            colend=adjust_for_midnight(gridEnd),
            rowstart=get_timecode(gridStart, "start"),
            rowend=get_timecode(gridEnd, "end"),
            short=(end-start <= timedelta(minutes=60)),
        )

def dates_array(firstDayThisWeek):
    dates = [[0]*7 for _ in range(total_weeks_loaded)]
    firstDayInArray = firstDayThisWeek - timedelta(weeks = load_past_weeks)
    counter = 0
    for i in range (0, total_weeks_loaded):
        for j in range (0, 7):
            dates[i][j] = (firstDayInArray + timedelta(days = counter)).day
            counter+=1
    return dates

def icon_number(user):
    return(int(user['icon'][-5:-4]))

def build_away_array(today, weeksEvents):
    day = {"00-00" : 0x000000, "00-15" : 0x000000, "00-30" : 0x000000, "00-45" : 0x000000, "01-00" : 0x000000, "01-15" : 0x000000, "01-30" : 0x000000, "01-45" : 0x000000, "02-00" : 0x000000, "02-15" : 0x000000, "02-30" : 0x000000, "02-45" : 0x000000, "03-00" : 0x000000, "03-15" : 0x000000, "03-30" : 0x000000, "03-45" : 0x000000, "04-00" : 0x000000, "04-15" : 0x000000, "04-30" : 0x000000, "04-45" : 0x000000, "05-00" : 0x000000, "05-15" : 0x000000, "05-30" : 0x000000, "05-45" : 0x000000, "06-00" : 0x000000, "06-15" : 0x000000, "06-30" : 0x000000, "06-45" : 0x000000, "07-00" : 0x000000, "07-15" : 0x000000, "07-30" : 0x000000, "07-45" : 0x000000, "08-00" : 0x000000, "08-15" : 0x000000, "08-30" : 0x000000, "08-45" : 0x000000, "09-00" : 0x000000, "09-15" : 0x000000, "09-30" : 0x000000, "09-45" : 0x000000, "10-00" : 0x000000, "10-15" : 0x000000, "10-30" : 0x000000, "10-45" : 0x000000, "11-00" : 0x000000, "11-15" : 0x000000, "11-30" : 0x000000, "11-45" : 0x000000, "12-00" : 0x000000, "12-15" : 0x000000, "12-30" : 0x000000, "12-45" : 0x000000, "13-00" : 0x000000, "13-15" : 0x000000, "13-30" : 0x000000, "13-45" : 0x000000, "14-00" : 0x000000, "14-15" : 0x000000, "14-30" : 0x000000, "14-45" : 0x000000, "15-00" : 0x000000, "15-15" : 0x000000, "15-30" : 0x000000, "15-45" : 0x000000, "16-00" : 0x000000, "16-15" : 0x000000, "16-30" : 0x000000, "16-45" : 0x000000, "17-00" : 0x000000, "17-15" : 0x000000, "17-30" : 0x000000, "17-45" : 0x000000, "18-00" : 0x000000, "18-15" : 0x000000, "18-30" : 0x000000, "18-45" : 0x000000, "19-00" : 0x000000, "19-15" : 0x000000, "19-30" : 0x000000, "19-45" : 0x000000, "20-00" : 0x000000, "20-15" : 0x000000, "20-30" : 0x000000, "20-45" : 0x000000, "21-00" : 0x000000, "21-15" : 0x000000, "21-30" : 0x000000, "21-45" : 0x000000, "22-00" : 0x000000, "22-15" : 0x000000, "22-30" : 0x000000, "22-45" : 0x000000, "23-00" : 0x000000, "23-15" : 0x000000, "23-30" : 0x000000, "23-45" : 0x000000}
    for event in weeksEvents:
        if (event['colstart'] == today.strftime("%A")):
            t = event['rowstart']
            while ((t != event['rowend']) and t != "00-00"):
                for person in event['attendees']:
                    day[t] = day[t] | (1 << (icon_number(person) - 1))
                t = increment_timecode(t)
    return(day)
                

def increment_timecode(timecode):
    if timecode == "23-45":
        return "00-00"
    if timecode[-2:] == "45":
        return((str(int(timecode[0:2]) + 1)).zfill(2)+ "-00")
    else:
        return(timecode[0:3] + (str(int(timecode[-2:]) + 15)).zfill(2))

def get_timecode(date, startEnd):
    if date.strftime("%H:%M") == "00:00":
        if startEnd == "start":
            return "00-00"
        else:
            return "-1"
    else:
        hour = date.hour
        minute = 15 * math.floor(date.minute / 15)
        if startEnd == "end":
            minute += 15
            if minute >= 60:
                hour += 1
                minute = minute % 60
        return "{}-{}".format(str(hour).zfill(2), (str(minute)).zfill(2))


def adjust_for_midnight(date):
    if date.strftime("%H:%M") == "00:00":
        return (date - timedelta(days=1)).strftime("%A")
    else:
        return date.strftime("%A")
