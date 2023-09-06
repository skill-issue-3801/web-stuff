from functools import wraps
from sqlalchemy import orm
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()
Session = DB.session
Session.expire_on_commit = False

class GlobalStuff(object):
    def __init__(self):
        self.events = []
        self.hashes = {}

    def set_events(self, new):
        self.events = new

    def set_hashes(self, new):
        self.hashes = new

Global = GlobalStuff()

def has_db(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        s = Session()
        s.expire_on_commit = False
        with s.begin_nested():
            result = fn(s, *args, **kwargs)
        s.commit()
        return result

    return decorated

def has_global_stuff(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        result = fn(Global, *args, **kwargs)
        return result

    return decorated