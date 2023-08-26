import logging

from flask import Blueprint

from .models import CalendarLocations
from .app import app

admin = Blueprint("admin", __name__)
logger = logging.getLogger(__name__)


@admin.route('/add_calendars', methods=["GET", "POST"], subdomain="<subdomain>")
def add_calendars():
    if request.method == "GET":
        return "<p>This is the page to add calendars.</p>"
    
    db_session = app.db_session()
    db_session.add(CalendarLocations(name="NAME", url="URL"))
    db_session.commit()
    db_session.close()
