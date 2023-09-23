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

            s.commit()
            s.close()        

    waitress.serve(app, host=args[1], port=9003)


