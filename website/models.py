from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class CalendarLocations(Base):
    family_member_name: Mapped[str] = mapped_column("name", String, primary_key=True)
    url: Mapped[str] = mapped_column("url", String, primary_key=True)
