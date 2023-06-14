from ..database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


class Faculty(Base):
    __tablename__ = "faculties"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship(Faculty, backref="departments")

    __table_args__ = (
        UniqueConstraint("faculty_id", "name", name="uq_faculty_department"),
    )


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship(Department, backref="groups")
