import logging

from flask import Blueprint, request

from .app import app


calendar = Blueprint("calendar", __name__)
logger = logging.getLogger(__name__)


@calendar.route("/", methods=["GET"])
def default():
    return """<p>The calendar page.</p>"""
