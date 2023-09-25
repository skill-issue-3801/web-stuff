import logging

import sqlalchemy
import waitress

from .app import app
from .admin import admin
from .calendar import calendar
from .base import Session, DB
from .models import Base, FamilyMember
from .cal import User

def main(db_url, args):
    logging.basicConfig(level=logging.INFO)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    with app.app_context():
        s = Session()
        Base.metadata.create_all(s.connection())
        s.commit()

    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(calendar, url_prefix="/calendar")

    if __debug__:
        with app.app_context():
            s = Session()
            
            name = "test"
            link = "https://calendar.google.com/calendar/ical/2ada2da9bfef0aa54436c6f7564871be2fb1bd6e9486595e4948b9469696d140%40group.calendar.google.com/public/basic.ics"
            calendarType = "google"
            email = "a@b.c"
            icon = "graphics/ocean-icons/Slug_1.png"
            eventsHash = 0
            userObject = User(name, link, calendarType, email)

            s.add(FamilyMember(
                name=name,
                url=link,
                calendarType=calendarType,
                email=email,
                icon=icon,
                eventsHash=eventsHash,
                userObject=userObject,
            ))

            s.add(FamilyMember(
                name="test 2",
                url="https://calendar.google.com/calendar/ical/406051a36534cc9f88d8df0d7fe1fb69dff521e5713ec771bc80e9d8e461f391%40group.calendar.google.com/private-3f7d09cd72dfeb37f715568fbb3ef85c/basic.ics",
                calendarType="google",
                email="a@c.b",
                icon="graphics/ocean-icons/Slug_2.png",
                eventsHash=eventsHash,
                userObject=userObject,
            ))
            name="testa"
            url="https://calendar.google.com/calendar/ical/8b3d1384c9c8c2b83d89bbdfc618e9643c020a37f917797154bb8bc15313d399%40group.calendar.google.com/private-61d6eaf479c9245fe2746f578b6d9b3b/basic.ics"
            calendarType="google"
            email=None
            icon="graphics/ocean-icons/Slug_1.png"
            eventsHash = 0
            userObject = User(name, url, calendarType, email)
            s.add(FamilyMember(name=name, url=url, calendarType=calendarType, email=email, icon=icon, eventsHash=eventsHash, userObject=userObject))
            
            name="testb"
            url="https://calendar.google.com/calendar/ical/9062b4ce5a3b1b15ba9e901454417dc0362a7576c967b63d7aa2e0e12561cf04%40group.calendar.google.com/private-b1725a4a26321058c715e75c353d80ae/basic.ics"
            icon="graphics/ocean-icons/Slug_2.png"
            userObject = User(name, url, calendarType, email)
            s.add(FamilyMember(name=name, url=url, calendarType=calendarType, email=email, icon=icon, eventsHash=eventsHash, userObject=userObject))
            
            name="testc"
            url="https://calendar.google.com/calendar/ical/8330378fae6a0e018310a99cde5b9a96bd5ae359059078593bfc4259181d1222%40group.calendar.google.com/private-618208b88c6b36f5a5f75460c71f4aaa/basic.ics"
            icon="graphics/ocean-icons/Slug_3.png"
            userObject = User(name, url, calendarType, email)
            s.add(FamilyMember(name=name, url=url, calendarType=calendarType, email=email, icon=icon, eventsHash=eventsHash, userObject=userObject))
            
            name="testd"
            url="https://calendar.google.com/calendar/ical/9a10fca10921df108cb568fe942ef0b1d75095228d164104ea3880d830e6defc%40group.calendar.google.com/private-1ad1b63e3255bc1a06b816d93ece94b6/basic.ics"
            icon="graphics/ocean-icons/Slug_4.png"
            userObject = User(name, url, calendarType, email)
            s.add(FamilyMember(name=name, url=url, calendarType=calendarType, email=email, icon=icon, eventsHash=eventsHash, userObject=userObject))
            
            name="teste"
            url=None
            calendarType=None
            icon="graphics/ocean-icons/Slug_5.png"
            userObject = User(name, url, 'none', email)
            s.add(FamilyMember(name=name, url=url, calendarType=calendarType, email=email, icon=icon, eventsHash=eventsHash, userObject=userObject))
            

            s.commit()
            s.close()        

    waitress.serve(app, host=args[1], port=9003)


