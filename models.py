from pydantic import BaseModel, EmailStr, UUID4, conint
from typing import List

class Grade(BaseModel):
    id: UUID4
    course: str
    score: conint(ge=0, le=100)

class Student(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: EmailStr
    grades: List[Grade]
