from ..database import Base
from sqlalchemy import (
    Column,
    Date,
    String,
    Integer,
    ForeignKey,
    Table,
    UniqueConstraint,
)

from sqlalchemy.orm import relationship
from .structure import Group, Department
from .education import Course, Exam


class UnivercityVisitor(Base):
    """Common model for person in univercity"""

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


class Teacher(UnivercityVisitor):
    __tablename__ = "teachers"
    id = Column(Integer, ForeignKey("visitors.id"), primary_key=True)
    courses = relationship(
        Course,
        secondary="teacher_course",
        back_populates="teachers",
        cascade="all, delete",
    )
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship(Department, backref="teachers")


class Student(UnivercityVisitor):
    __tablename__ = "students"
    id = Column(Integer, ForeignKey("visitors.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    group = relationship(Group, backref="students")
    exams = relationship(
        Exam,
        secondary="students_exams",
        back_populates="students",
        cascade="all, delete",
    )
    courses = relationship(
        Course, secondary="students_courses", back_populates="students"
    )
