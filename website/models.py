from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class CalendarLocations(Base):
    __tablename__ = "calendars"

    family_member_name: Mapped[str] = mapped_column("name", String, primary_key=True)
    url: Mapped[str] = mapped_column("url", String, primary_key=True)


class Settings(Base):
    __tablename__ = "settings"

    setting_name: Mapped[str] = mapped_column("key", String, primary_key=True)
    setting_value: Mapped[str] = mapped_column("val", String)


class Family(Base):
    __tablename__ = "family"

    name: Mapped[str] = mapped_column("name", String)
    icon: Mapped[str] = mapped_column("icon", String)
    gmail: Mapped[str] = mapped_column("email", String, primary_key=True)
