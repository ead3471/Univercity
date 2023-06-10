from .database import Base
from sqlalchemy import (
    TIMESTAMP,
    Column,
    Date,
    String,
    Boolean,
    Integer,
    text,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship


class UnivercityVisitor(Base):
    __tablename__ = "visitors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    passport_id = Column(String, nullable=False)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


teacher_course = Table(
    "teacher_course",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
)


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    visitor_id = Column(Integer, ForeignKey("visitors.id"))
    courses = relationship(
        "Course", secondary="teacher_course", back_populates="teachers"
    )


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(
        String,
        nullable=False,
    )
    teachers = relationship(
        "Teacher", secondary="teacher_course", back_populates="courses"
    )


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    visitor_id = Column(Integer, ForeignKey("visitors.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", backref="students")
