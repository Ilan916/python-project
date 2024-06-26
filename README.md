# API de Gestion des Étudiants

Ce projet est réalisé avec Poetry et FastAPI. Il fournit une API simple pour gérer les étudiants et leurs notes.

## Vue d'ensemble du projet

- **FastAPI** : Un framework web moderne et rapide pour construire des APIs avec Python 3.6+.
- **Poetry** : Gestion des dépendances et packaging de Python simplifiés.

## Documentation de l'API

Vous pouvez accéder à la documentation Swagger pour FastAPI à l'URL suivante :

[Documentation Swagger FastAPI](http://127.0.0.1:8000/docs)

## URL de l'application

L'application fonctionne à l'URL suivante :

[URL de l'application](http://127.0.0.1:8000)

## Installation

Pour installer les dépendances, exécutez la commande suivante :

```bash
poetry install
```

## Lancement

```bash
poetry run uvicorn main:app --reload
```

## Endpoints de l'API

## Créer un étudiant
Pour créer un nouvel étudiant, utilisez la commande curl suivante :

```bash
curl -X POST "http://127.0.0.1:8000/student/" -H "Content-Type: application/json" -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com",
    "grades": [
        {"course": "maths", "score": 12},
        {"course": "science", "score": 15}
    ]
}'
```
## Récupérer un étudiant
Pour récupérer un étudiant par son ID, utilisez la commande curl suivante :

```bash
curl -X GET "http://127.0.0.1:8000/student/{student_id}"
```
## Supprimer un étudiant
Pour supprimer un étudiant par son ID, utilisez la commande curl suivante :

```bash
curl -X DELETE "http://127.0.0.1:8000/student/{student_id}"
```

## Récupérer une note
Pour récupérer une note spécifique pour un étudiant par son ID étudiant et ID de note, utilisez la commande curl suivante :

```bash
curl -X GET "http://127.0.0.1:8000/student/{student_id}/grades/{grade_id}"
```

## Supprimer une note
Pour supprimer une note spécifique pour un étudiant par son ID étudiant et ID de note, utilisez la commande curl suivante :

```bash
curl -X DELETE "http://127.0.0.1:8000/student/{student_id}/grades/{grade_id}"
```
## Exporter en CSV
Pour exporter la liste des étudiants en format csv

```bash
curl -X GET "http://127.0.0.1:8000/export?format=csv"
```

## Exporter en JSON 
Pour exporter la liste des étudiants en format json

```bash
curl -X GET "http://127.0.0.1:8000/export?format=json"
```

## Exemple
Voici un exemple concret d'utilisation des commandes curl et des types de réponses attendues.



