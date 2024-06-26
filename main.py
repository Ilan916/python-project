from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr, UUID4, conint
from typing import List, Optional
from uuid import uuid4

app = FastAPI()

@app.get("/{name}", response_class=HTMLResponse)
def read_root(name: str):
    return f"<h1>Hello <span>{name}</span></h1>"

class Grade(BaseModel):
    id: Optional[UUID4] = None
    course: str
    score: conint(ge=0, le=100)

class Student(BaseModel):
    id: Optional[UUID4] = None
    first_name: str
    last_name: str
    email: EmailStr
    grades: List[Grade]

students = {}

@app.post("/student/", response_model=UUID4)
def create_student(student: Student):
    student.id = student.id or uuid4()
    # Assurez-vous que chaque grade a un UUID
    for grade in student.grades:
        grade.id = grade.id or uuid4()
    students[student.id] = student
    return student.id

@app.get("/student/{identifier}", response_model=Student)
def get_student(identifier: UUID4):
    student = students.get(identifier)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.delete("/student/{identifier}")
def delete_student(identifier: UUID4):
    if identifier not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[identifier]
    return {"detail": "Student deleted"}

@app.get("/student/{identifier}/grades/{grade_id}", response_model=Grade)
def get_grade(identifier: UUID4, grade_id: UUID4):
    student = students.get(identifier)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for grade in student.grades:
        if grade.id == grade_id:
            return grade
    raise HTTPException(status_code=404, detail="Grade not found")

@app.delete("/student/{identifier}/grades/{grade_id}")
def delete_grade(identifier: UUID4, grade_id: UUID4):
    student = students.get(identifier)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.grades = [grade for grade in student.grades if grade.id != grade_id]
    return {"detail": "Grade deleted"}

