from pydantic import BaseModel, Field


class CourseSchema(BaseModel):
    name: str = Field(description="Course name")
