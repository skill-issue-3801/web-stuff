from sqlalchemy import Integer, PickleType, String, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Settings(Base):
    __tablename__ = "settings"

    setting_name = Column("key", String, primary_key=True)
    setting_value = Column("val", String)


class FamilyMember(Base):
    __tablename__ = "familymembers"

    name = Column("name", String, primary_key=True)
    url = Column("url", String, unique=True, nullable=True)
    calendartype = Column("calendartype", String, nullable=True)
    email = Column("email", String, nullable=True, unique=True)
    # string for path to icon image
    icon = Column("icon", String, nullable=False)
    # hash of a string of this users' events, used to quickly check if there have been any changes
    # since last checked to avoid re-processing
    eventshash = Column("eventshash", Integer, nullable=False)
    # pickled python object of class User
    userobject = Column("userobject", PickleType, nullable=False)
