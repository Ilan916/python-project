from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, EmailStr, UUID4, conint
from typing import List, Optional
from uuid import uuid4
from io import StringIO
import csv

app = FastAPI()

@app.get("/export")
def export_data(format: str = "csv"):
    if format == "json":
        return students
    elif format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "first_name", "last_name", "email", "grades"])
        for student in students.values():
            grades = "; ".join([f"{grade.course}:{grade.score}" for grade in student.grades])
            writer.writerow([student.id, student.first_name, student.last_name, student.email, grades])
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv")
    else:
        raise HTTPException(status_code=400, detail="Invalid format")

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


