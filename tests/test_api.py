import os
import json
import pytest
from fastapi.testclient import TestClient
from uuid import UUID, uuid4
from main import app, DATA_FILE, Student

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_data():
    # Clear the data.json file before each test
    with open(DATA_FILE, "w") as file:
        json.dump({"students": []}, file)

def load_data():
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4, default=str)

def test_read_root():
    response = client.get("/John")
    assert response.status_code == 200
    assert response.text == "<h1>Hello <span>John</span></h1>"

def test_create_student(clear_data):
    # Créer un étudiant de test
    student_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "grades": []
    }

    # Envoyer une requête POST pour créer l'étudiant
    response = client.post("/student/", json=student_data)

    # Vérifier que la requête a réussi (code de statut HTTP 200)
    assert response.status_code == 200

    # Obtenir l'ID de l'étudiant créé depuis la réponse JSON
    student_id = response.json()

    # Charger les données du fichier JSON
    data = load_data()

    # Vérifier que l'ID de l'étudiant est dans les données
    assert any(student["id"] == student_id for student in data["students"])

    # Vérifier que les détails de l'étudiant créé sont corrects
    created_student = next(student for student in data["students"] if student["id"] == student_id)
    assert created_student["first_name"] == student_data["first_name"]
    assert created_student["last_name"] == student_data["last_name"]
    assert created_student["email"] == student_data["email"]
    assert created_student["grades"] == student_data["grades"]
