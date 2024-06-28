from pydantic import BaseModel, EmailStr, conint
from typing import List, Optional
from uuid import UUID

class Grade(BaseModel):
    id: Optional[UUID] = None
    course: str
    score: conint(ge=0, le=100)

class Student(BaseModel):
    id: Optional[UUID] = None
    first_name: str
    last_name: str
    email: EmailStr
    grades: List[Grade]
