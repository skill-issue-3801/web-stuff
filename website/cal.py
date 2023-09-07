import pytz 
import validators
from datetime import datetime, timedelta
from icalevents import icalevents, icalparser

accepted_calendars = ['google', 'apple']

class User:
    """ An object representing a user/family member
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
    def __init__(self, name, calendar_link, caltype, email=None):
        self._name = name
        self._calendar_link = calendar_link
        self._caltype = caltype
        if email and email[0:7] != "mailto:":
            self._email = "mailto:" + email
        else:
            self._email = email
        self._event_list = []
        self._events_hash = 0
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






def is_google_url(url):
    """ Check if the given string is a valid google calendar url

    Args:
        url (string): The url to check

    Returns:
        Bool: Return True if the string is a valid google calendar url, False otherwise.
    """
    
    if (validators.url(url.strip()) and
        url[0:42] == "https://calendar.google.com/calendar/ical/" and 
        url[-10:] == "/basic.ics"):
        return True
    return False
        
def is_apple_url(url):
    """ Check if the given string is a valid apple calendar url

    Args:
        url (string): The url to check

    Returns:
        Bool: Return True if the string is a valid apple calendar url, False otherwise.
    """
    if (url[0:42] == "webcal://p122-caldav.icloud.com/published/"):
        return True
    return False
     
def events_get_hash(events):
    uidstr = ""
    for event in events:
        uidstr += str(event)
    return(hash(uidstr))

def add_user(names, urls, emails, name, caltype, url, email = None):
    if name in names:
        print("Sorry, a user by that name already exists. Names must be unique")
        return False
    
    if url in urls:
        print("Sorry, another user is already using that calendar! Everyone must have their own calendar")
        return False
    
    if email and email in emails:
        print("Sorry, a user is already associated with this email: ", email)
        return False
    
    if caltype not in accepted_calendars:
        print("Sorry, ", caltype, " is not an accepted calendar type")
        return False
    
    if ((caltype == "google" and not is_google_url(url)) or 
                (caltype == "apple" and not is_apple_url(url))):
        print("Sorry, that is not a valid ", caltype, " calendar url")
        return False
    
    if email != None and not validators.email(email.strip()):
        print("Sorry, that is not a valid email address")
        return False
    
    newUser = User(name, url.strip(), caltype, email)
    print("added ", name)
    return newUser


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
        if ((caltype == "google" and is_google_url(newLink)) or (caltype == "apple" and is_apple_url(newLink))):
            # acceptable, update their cal and return them
            user.set_link(newLink, caltype)
            return True
        else:
            print("Sorry, ", newLink, "is not a valid ", caltype, "calendar url")
            return False
    else:
        print("Sorry, ", caltype, " is not an accepted calendar type, must be 'apple' or 'google'")
        return False
 
# I AM CONSIDERING SCRAPPING THIS FOR SIMPLICITY, IF THEY REALLY WANT TO THEY CAN JUST DELETE AND MAKE A NEW USER   
def update_user_name(names, name, newName, user):
    if not name in names:
        print("There is no user by the name ", name, "to edit")
        return False
    
    if newName in names:
        print("There is another user already using the name", newName, ", names must be unique")
        return False
    
    user.set_name(newName)
    print("Warning: events where", newName, "was invited by tagging them in the description"
            " using their old name will not appear unless you update them in your calendar!")
    return True     







"""
this thing is gonna be used like:
changes = False
today = blahblahblah
hashes = {}
for row in FamilyMembers table:
    newHash = check_cal_for_updates(row.url, row.caltype, row.hash, today)
    if newHash = False:
        hashes[row.name] = hash
    else:
        hashes[row.name] = newHash
        changes = True

if changes == True:
    <unpickle users>
    newEvents = update_events(<array of unpickled users>, today, hashes)
    for row in FamilyMembers table:
        <extract changes from user object and update table entries>
        <re-pickle user and store>
    <update events table with newEvents, there will be overlap>
else:
    all good, no changes needed
"""

def check_cal_for_updates(url, caltype, hash, today):
    evs = icalevents.events(url=url, start=(today - timedelta(days=14)), 
            end = (today + timedelta(days=14)), sort = True, fix_apple=(caltype == 'apple'))
    evshash = events_get_hash(evs)
    if evshash == hash:
        return False # no update needed
    return evshash # this user has some changes to apply

def update_events(family, today, hashes, names, emails):
    return_events = []
    for member in family:
        if hashes[member.get_name()] == member.get_hash():
            # their events have not chnaged, we will still check if they attend anything though
            return_events.extend(member.get_events())
        else:
            # their evenys have changed somehow, reprocess
            member.set_hash(hashes[member.get_name()]) # record hash of events before processing
            evs = icalevents.events(url=member.get_link(), start=(today - timedelta(days=14)), 
                    end = (today + timedelta(days=14)), sort = True, fix_apple=(member.get_caltype() == 'apple'))
            for event in evs:
                if (process_attendees(member.get_name(), event, family, names, emails)):
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
    """ Process the detected attendees and anyone named in the first line of the 
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
    if (event.organizer != None): # has invitees, add them before adding from description
        if event.organizer == None: # no attendees added
            org_name = calowner
        elif event.organizer in emails: # attendees addded and was made by someone in family
            org_name = get_email_owner(event.organizer, family)
        else: # attendees added and organised by someone outside family, give this event to calowner
            org_name = calowner
          
        if (org_name == calowner): # event organised by the owner of this calendar
            event.attendee.add(calowner) # add organiser
            if type(cpy_att) == list: 
                # if there are many attendees, add all
                for att in cpy_att:
                    user_name = get_email_owner(att, family)
                    if user_name != None: # if this email belongs to a family member
                        event.attendee.add(user_name)
            elif type(cpy_att) == icalparser.Attendee: 
                # if there is 1 attendee
                user_name = get_email_owner(att, family)
                if user_name != None: # add them if they are family
                    event.attendee.add(user_name)      
        else: # event organised by another family member, we will append form their calendar
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
     