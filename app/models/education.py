from ..database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Date,
    Time,
    CheckConstraint,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .buildings import Auditory

# Table for many to many link between students and courses
students_courses = Table(
    "students_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
    UniqueConstraint("student_id", "course_id", name="uq_student_course"),
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
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("Faculty", backref="courses")

    # many to many link with students
    students = relationship(
        "Student",
        secondary=students_courses,
        back_populates="courses",
        cascade="all, delete",
    )

    # many to many link with education plans
    plans = relationship(
        "EducationPlan", secondary="plans_courses", back_populates="courses"
    )


class CourseProgramm(Base):
    __tablename__ = "course_programms"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    description = Column(Text)
    course_id = Column(Integer, ForeignKey("courses.id"), unique=True)
    course = relationship(Course, backref="programms")


class CourseProgrammTheme(Base):
    __tablename__ = "course_programms_themes"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    description = Column(Text)
    duration = Column(Integer)
    course_programm_id = Column(Integer, ForeignKey("course_programms.id"))
    course_programm = relationship(CourseProgramm, backref="themes")


# table for many to many link between students and exams
students_exams = Table(
    "students_exams",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("exam_id", Integer, ForeignKey("exams.id")),
    UniqueConstraint("student_id", "exam_id", name="uq_student_exam"),
)


class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship(Course, backref="exams")
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", backref="exams")
    start = Column(DateTime)
    end = Column(DateTime)
    students = relationship(
        "Student", secondary="students_exams", back_populates="exams"
    )


class ExamGrade(Base):
    __tablename__ = "exam_grades"
    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    exam = relationship(Exam, backref="grades")
    # TODO: to settings :
    score = Column(
        Integer,
        CheckConstraint("score >= 0 AND score <= 5", name="score_limit"),
    )
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", backref="exam_grades")


class CourseGrade(Base):
    __tablename__ = "course_grades"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship(Course, backref="courses")
    # TODO: to settings :
    score = Column(
        Integer,
        CheckConstraint("score >= 0 AND score <= 5", name="score_limit"),
    )
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", backref="course_grades")
    UniqueConstraint("student_id", "course_id", name="uq_student_course")


class Homework(Base):
    __tablename__ = "homeworks"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship(Course, backref="homeworks")
    created = Column(
        DateTime,
    )
    text = Column(Text)


class Semester(Base):
    __tablename__ = "semesters"
    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    number = Column(Integer)


plans_courses = Table(
    "plans_courses",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.id")),
    Column("plan_id", Integer, ForeignKey("education_plans.id")),
    UniqueConstraint("course_id", "plan_id", name="uq_course_plan"),
)


class EducationPlan(Base):
    __tablename__ = "education_plans"
    id = Column(Integer, primary_key=True)
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    semester = relationship(Semester, backref="plans")
    courses = relationship(
        Course,
        secondary=plans_courses,
        back_populates="plans",
        cascade="all, delete",
    )
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", backref="plans")


class TimeSlot(Base):
    __tablename__ = "timeslots"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=64), unique=True)
    start = Column(Time)
    end = Column(Time)


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("shedules.id"))
    schedule = relationship("Schedule", backref="lessons")
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship(Course, backref="lessons")
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", backref="lessons")
    timeslot_id = Column(Integer, ForeignKey("timeslots.id"))
    timeslot = relationship(TimeSlot, backref="lessons")
    auditory_id = Column(Integer, ForeignKey("auditories.id"))
    auditory = relationship(Auditory, backref="lessons")

    __table_args__ = (
        UniqueConstraint(
            "timeslot_id",
            "auditory_id",
            "schedule_id",
            name="uq_time_auditory_date",
        ),
    )


class Schedule(Base):
    __tablename__ = "shedules"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", backref="schedules")

    __table_args__ = (
        UniqueConstraint("group_id", "date", name="uq_group_date"),
    )
