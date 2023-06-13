from pydantic import BaseModel, Field


class GroupSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True
