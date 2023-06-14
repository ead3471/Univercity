from ..database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.orm import relationship


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True)
    street = Column(String(length=50))
    house_number = Column(String(length=10))


class Auditory(Base):
    __tablename__ = "auditories"
    id = Column(Integer, primary_key=True)
    room_number = Column(String(length=10))
    building_id = Column(Integer, ForeignKey("buildings.id"))
    building = relationship(Building, backref="auditories")
    __table_args__ = (
        UniqueConstraint(
            "room_number", "building_id", name="uq_room_building"
        ),
    )
