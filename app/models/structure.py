from ..database import Base
from sqlalchemy import (
    Column,
    Date,
    String,
    Boolean,
    Integer,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
