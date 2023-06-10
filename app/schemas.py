from datetime import datetime, date
from pydantic import BaseModel, constr, validator, Field
import re
from typing import Optional, List


class VisitorBaseSchema(BaseModel):
    name: str = Field(description="Visitor name", max_length=16)
    middle_name: str = Field(description="Visitor middle name", max_length=16)
    last_name: str = Field(description="Visitor last name", max_length=16)
    passport_id: str = Field(
        description="Visitor passport id", regex=r"^\d{4} \d{6}$"
    )
    birthdate: date = Field(description="Visitor birthdate")


class CreateVisitorSchema(VisitorBaseSchema):
    pass


class Visitor(VisitorBaseSchema):
    class Config:
        orm_mode = True


class CreateStudentSchema(VisitorBaseSchema):
    group_id: int = Field(description="Group id")


class Student(VisitorBaseSchema):
    id: int = Field(description="Student id")
    group: Optional[int] = Field(description="Group name")


class CreateTeacherSchema(VisitorBaseSchema):
    courses: List[int] = Field(description="Teachers courses")


class Course(BaseModel):
    name: str = Field(description="Course name")


class Teacher(Visitor):
    id: int = Field(description="Student id")
    courses: Optional[List[Course]] = Field(description="Courses")
