from ..database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


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
