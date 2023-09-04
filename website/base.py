from functools import wraps
from sqlalchemy import orm
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()
Session = DB.session
Session.expire_on_commit = False


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
