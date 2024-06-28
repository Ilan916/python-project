import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from typing import List
from uuid import uuid4, UUID
from io import StringIO
import csv
from Models.models import Grade, Student

app = FastAPI()
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"students": []}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4, default=str)




@app.get("/export")
def export_data(format: str = "csv"):
    data = load_data()
    students = data["students"]
    if format == "json":
        return students
    elif format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "first_name", "last_name", "email", "grades"])
        for student in students:
            grades = "; ".join([f"{grade['course']}:{grade['score']}" for grade in student["grades"]])
            writer.writerow([student["id"], student["first_name"], student["last_name"], student["email"], grades])
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv")
    else:
        raise HTTPException(status_code=400, detail="Invalid format")        

@app.get("/{name}", response_class=HTMLResponse)
def read_root(name: str):
    return f"<h1>Hello <span>{name}</span></h1>"

@app.post("/student/", response_model=UUID)
def create_student(student: Student):
    data = load_data()
    student.id = uuid4()
    for grade in student.grades:
        grade.id = uuid4()
    data["students"].append(student.model_dump())
    save_data(data)
    return student.id

@app.get("/student/{student_id}", response_model=Student)
def get_student(student_id: UUID):
    data = load_data()
    for student in data["students"]:
        if student["id"] == str(student_id):
            return Student(**student)
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/student/{student_id}")
def delete_student(student_id: UUID):
    data = load_data()
    for student in data["students"]:
        if student["id"] == str(student_id):
            data["students"].remove(student)
            save_data(data)
            return {"detail": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found")

@app.get("/student/{student_id}/grades/{grade_id}", response_model=Grade)
def get_grade(student_id: UUID, grade_id: UUID):
    data = load_data()
    for student in data["students"]:
        if student["id"] == str(student_id):
            for grade in student["grades"]:
                if grade["id"] == str(grade_id):
                    return Grade(**grade)
            raise HTTPException(status_code=404, detail="Grade not found")
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/student/{student_id}/grades/{grade_id}")
def delete_grade(student_id: UUID, grade_id: UUID):
    data = load_data()
    for student in data["students"]:
        if student["id"] == str(student_id):
            for grade in student["grades"]:
                if grade["id"] == str(grade_id):
                    student["grades"].remove(grade)
                    save_data(data)
                    return {"detail": "Grade deleted"}
            raise HTTPException(status_code=404, detail="Grade not found")
    raise HTTPException(status_code=404, detail="Student not found")


