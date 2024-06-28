# tests/test_api.py

from fastapi.testclient import TestClient
from uuid import UUID, uuid4
from main import app, create_student, students, Student, Grade

client = TestClient(app)

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

# Teste la récupération d'un étudiant par son identifiant
def test_get_student():
    # Ajouter un étudiant de test directement dans students pour le tester
    student_id = uuid4()
    students[student_id] = Student(
        id=student_id,
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        grades=[]
    )

    # Envoyer une requête GET pour obtenir l'étudiant par son ID
    response = client.get(f"/student/{student_id}")

    # Vérifier que la requête a réussi (code de statut HTTP 200)
    assert response.status_code == 200

    # Vérifier que les détails de l'étudiant récupéré sont corrects
    retrieved_student = response.json()
    assert retrieved_student["id"] == str(student_id)  # Convertir UUID en str pour la comparaison
    assert retrieved_student["first_name"] == students[student_id].first_name
    assert retrieved_student["last_name"] == students[student_id].last_name
    assert retrieved_student["email"] == students[student_id].email
    assert retrieved_student["grades"] == students[student_id].grades

# Teste la tentative de récupération d'un étudiant inexistant
def test_get_nonexistent_student():
    response = client.get(f"/student/{uuid4()}")
    assert response.status_code == 404

def test_delete_student():
    # Ajouter un étudiant de test directement dans students pour le supprimer ensuite
    student_id: UUID = uuid4()
    students[student_id] = Student(
        id=student_id,
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        grades=[]
    )

    # Envoyer une requête DELETE pour supprimer l'étudiant par son ID
    response = client.delete(f"/student/{student_id}")

    # Vérifier que la requête a réussi (code de statut HTTP 200)
    assert response.status_code == 200

    # Vérifier que l'étudiant a été effectivement supprimé de students
    assert student_id not in students.keys()

# Teste la tentative de suppression d'un étudiant inexistant
def test_delete_nonexistent_student():
    response = client.delete(f"/student/{uuid4()}")
    assert response.status_code == 404


# Teste la récupération d'une note spécifique d'un étudiant
def test_get_grade_student_not_found():
    # Envoyer une requête GET pour récupérer une note d'un étudiant inexistant
    non_existing_student_id = uuid4()
    non_existing_grade_id = uuid4()
    response = client.get(f"/student/{non_existing_student_id}/grades/{non_existing_grade_id}")

    # Vérifier que la requête retourne un statut 404 (étudiant non trouvé)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_get_grade_grade_not_found():
    # Ajouter un étudiant sans note pour le tester
    student_id = uuid4()
    students[student_id] = Student(
        id=student_id,
        first_name="John",
        last_name="Smith",
        email="john.smith@example.com",
        grades=[]
    )

    # Envoyer une requête GET pour récupérer une note inexistante pour l'étudiant
    non_existing_grade_id = uuid4()
    response = client.get(f"/student/{student_id}/grades/{non_existing_grade_id}")

    # Vérifier que la requête retourne un statut 404 (note non trouvée)
    assert response.status_code == 404
    assert response.json()["detail"] == "Grade not found"


def test_delete_grade():
    # Ajouter un étudiant avec des notes pour le tester
    student_id = uuid4()
    grade_id_1 = uuid4()
    grade_id_2 = uuid4()
    students[student_id] = Student(
        id=student_id,
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        grades=[
            Grade(id=grade_id_1, course="Math", score=85),
            Grade(id=grade_id_2, course="Science", score=92)
        ]
    )

    # Envoyer une requête DELETE pour supprimer une note spécifique de l'étudiant
    response = client.delete(f"/student/{student_id}/grades/{grade_id_1}")

    # Vérifier que la requête a réussi (code de statut HTTP 200)
    assert response.status_code == 200

    # Vérifier que la note a été correctement supprimée
    assert grade_id_1 not in [grade.id for grade in students[student_id].grades]
    assert grade_id_2 in [grade.id for grade in students[student_id].grades]  # Vérifier que l'autre note est toujours présente

def test_delete_grade_student_not_found():
    # Envoyer une requête DELETE pour supprimer une note d'un étudiant inexistant
    non_existing_student_id = uuid4()
    non_existing_grade_id = uuid4()
    response = client.delete(f"/student/{non_existing_student_id}/grades/{non_existing_grade_id}")

    # Vérifier que la requête retourne un statut 404 (étudiant non trouvé)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_delete_grade_grade_not_found():
    # Ajouter un étudiant sans note pour le tester
    student_id = uuid4()
    students[student_id] = Student(
        id=student_id,
        first_name="John",
        last_name="Smith",
        email="john.smith@example.com",
        grades=[]
    )

    # Envoyer une requête DELETE pour supprimer une note inexistante de l'étudiant
    non_existing_grade_id = uuid4()
    response = client.delete(f"/student/{student_id}/grades/{non_existing_grade_id}")

    # Vérifier que la requête retourne un statut 404 (note non trouvée)
    assert response.status_code == 404
    assert response.json()["detail"] == "Grade not found"
    #une erreur dans la function 'delete_grade' a été corrigé grace à ce test



