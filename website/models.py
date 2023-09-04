from sqlalchemy import String, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CalendarLocations(Base):
    __tablename__ = "calendars"

    family_member_name = Column("name", String, primary_key=True)
    url = Column("url", String, primary_key=True)


class Settings(Base):
    __tablename__ = "settings"

    setting_name = Column("key", String, primary_key=True)
    setting_value = Column("val", String)


class Family(Base):
    __tablename__ = "family"

    name = Column("name", String)
    icon = Column("icon", String)
    gmail = Column("email", String, primary_key=True)
