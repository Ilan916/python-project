from fastapi.testclient import TestClient
from uuid import UUID, uuid4
from main import app, create_student, students, Student

client = TestClient(app)

# Teste la route de base pour s'assurer qu'elle renvoie le bon message HTML
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

    # Vérifier que l'ID de l'étudiant est dans la liste des étudiants
    assert UUID(student_id) in students.keys()

    # Vérifier que les détails de l'étudiant créé sont corrects
    created_student = students[UUID(student_id)]
    assert created_student.first_name == student_data["first_name"]
    assert created_student.last_name == student_data["last_name"]
    assert created_student.email == student_data["email"]
    assert created_student.grades == student_data["grades"]

    