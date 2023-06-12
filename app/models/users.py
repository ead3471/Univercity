from ..database import Base
from sqlalchemy import (
    Column,
    Date,
    String,
    Boolean,
    Integer,
    ForeignKey,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from .structure import Group
from .education import Course


class UnivercityVisitor(Base):
    __tablename__ = "visitors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    passport_id = Column(String, nullable=False, unique=True)


teacher_course = Table(
    "teacher_course",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
    UniqueConstraint("teacher_id", "course_id", name="uq_teacher_course"),
)


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    visitor_id = Column(Integer, ForeignKey("visitors.id"))
    visitor = relationship(UnivercityVisitor)
    courses = relationship(
        Course,
        secondary="teacher_course",
        back_populates="teachers",
        cascade="all, delete",
    )


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    visitor_id = Column(Integer, ForeignKey("visitors.id"))
    visitor = relationship(UnivercityVisitor)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship(Group, backref="students")
