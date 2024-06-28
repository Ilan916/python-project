import os
import json
import pytest
from fastapi.testclient import TestClient
from uuid import UUID, uuid4
from main import app, DATA_FILE, Student, Grade

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

def test_create_student():
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

def test_get_student():
    # Ajouter un étudiant de test directement dans le fichier JSON pour le tester
    student_id = str(uuid4())
    student_data = {
        "id": student_id,
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "grades": []
    }
    data = load_data()
    data["students"].append(student_data)
    save_data(data)

    # Envoyer une requête GET pour obtenir l'étudiant par son ID
    response = client.get(f"/student/{student_id}")

    # Vérifier que la requête a réussi (code de statut HTTP 200)
    assert response.status_code == 200

    # Vérifier que les détails de l'étudiant récupéré sont corrects
    retrieved_student = response.json()
    assert retrieved_student["id"] == student_id
    assert retrieved_student["first_name"] == student_data["first_name"]
    assert retrieved_student["last_name"] == student_data["last_name"]
    assert retrieved_student["email"] == student_data["email"]
    assert retrieved_student["grades"] == student_data["grades"]

def test_delete_student():
    # Ajouter un étudiant de test directement dans le fichier JSON pour le supprimer ensuite
    student_id = str(uuid4())
    student_data = {
        "id": student_id,
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "grades": []
    }
    data = load_data()
    data["students"].append(student_data)
    save_data(data)

    # Envoyer une requête DELETE pour supprimer l'étudiant par son ID
    response = client.delete(f"/student/{student_id}")

    # Vérifier que la requête a réussi (code de statut HTTP 200)
    assert response.status_code == 200

    # Charger les données du fichier JSON
    data = load_data()

    # Vérifier que l'étudiant a été effectivement supprimé du fichier JSON
    assert not any(student["id"] == student_id for student in data["students"])

def test_get_grade_student_not_found():
    # Envoyer une requête GET pour récupérer une note d'un étudiant inexistant
    non_existing_student_id = str(uuid4())
    non_existing_grade_id = str(uuid4())
    response = client.get(f"/student/{non_existing_student_id}/grades/{non_existing_grade_id}")

    # Vérifier que la requête retourne un statut 404 (étudiant non trouvé)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_get_grade_grade_not_found():
    # Ajouter un étudiant sans note pour le tester
    student_id = str(uuid4())
    student_data = {
        "id": student_id,
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@example.com",
        "grades": []
    }
    data = load_data()
    data["students"].append(student_data)
    save_data(data)

    # Envoyer une requête GET pour récupérer une note inexistante pour l'étudiant
    non_existing_grade_id = str(uuid4())
    response = client.get(f"/student/{student_id}/grades/{non_existing_grade_id}")

    # Vérifier que la requête retourne un statut 404 (note non trouvée)
    assert response.status_code == 404
    assert response.json()["detail"] == "Grade not found"

def test_delete_grade():
    # Ajouter un étudiant avec des notes pour le tester
    student_id = str(uuid4())
    grade_id_1 = str(uuid4())
    grade_id_2 = str(uuid4())
    student_data = {
        "id": student_id,
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "grades": [
            {"id": grade_id_1, "course": "Math", "score": 85},
            {"id": grade_id_2, "course": "Science", "score": 92}
        ]
    }
    data = load_data()
    data["students"].append(student_data)
    save_data(data)

    # Envoyer une requête DELETE pour supprimer une note spécifique de l'étudiant
    response = client.delete(f"/student/{student_id}/grades/{grade_id_1}")

    # Vérifier que la requête a réussi (code de statut HTTP 200)
    assert response.status_code == 200

    # Charger les données du fichier JSON
    data = load_data()

    # Vérifier que la note a été correctement supprimée
    updated_student = next(student for student in data["students"] if student["id"] == student_id)
    assert grade_id_1 not in [grade["id"] for grade in updated_student["grades"]]
    assert grade_id_2 in [grade["id"] for grade in updated_student["grades"]]  # Vérifier que l'autre note est toujours présente

def test_delete_grade_student_not_found():
    # Envoyer une requête DELETE pour supprimer une note d'un étudiant inexistant
    non_existing_student_id = str(uuid4())
    non_existing_grade_id = str(uuid4())
    response = client.delete(f"/student/{non_existing_student_id}/grades/{non_existing_grade_id}")

    # Vérifier que la requête retourne un statut 404 (étudiant non trouvé)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"
