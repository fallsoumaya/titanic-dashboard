# Titanic Dashboard — Streamlit & DevOps Pipeline

## Description du projet
Ce projet consiste à développer un **dashboard interactif Streamlit** basé sur le dataset Titanic, puis à appliquer un **cycle DevOps complet** autour de l’application :
- versionnement avec Git
- tests automatisés
- conteneurisation Docker
- intégration continue (CI)
- monitoring des logs utilisateurs (ELK – démonstration)

L’objectif n’est pas de construire un modèle de machine learning complexe, mais de **livrer une application data prête à être exploitée**, testée, déployée et monitorée.

---

## Fonctionnalités principales
- Visualisation du dataset Titanic
- Analyse de survie (sexe, classe, âge)
- Filtres interactifs
- Export CSV
- Journalisation des interactions utilisateurs (logs JSON)

---

## Architecture du projet

titanic-dashboard/
│
├── app.py                  # Application Streamlit
├── data/
│   └── loader.py           # Chargement des données
├── tests/
│   └── test_loader.py      # Tests unitaires (pytest)
├── logs/
│   └── app.log             # Logs utilisateurs (JSON)
│
├── Dockerfile              # Conteneurisation
├── requirements.txt
│
├── .github/workflows/
│   └── ci.yml              # Pipeline CI/CD GitHub Actions
│
├── elk/
│   ├── docker-compose.yml  # Mini stack ELK (Elasticsearch, Kibana, Filebeat)
│   └── filebeat.yml
│
└── README.md

---

## Cloner le projet

```bash
git clone https://github.com/fallsoumaya/titanic-dashboard.git
cd titanic-dashboard

---

## Lancer l’application en local (sans Docker)

1️- Créer et activer un environnement virtuel
python -m venv env

- Windows

env\Scripts\activate

Linux / macOS

source env/bin/activate

2️- Installer les dépendances
pip install -r requirements.txt

3️- Lancer l’application Streamlit
streamlit run app.py
Application accessible sur : http://localhost:8501

Exécuter les tests unitaires
Les tests sont écrits avec pytest.
pytest -v

---

## Lancer l’application avec Docker

1- Construire l’image Docker
docker build -t titanic-dashboard .

2️- Lancer le conteneur
docker run -p 8501:8501 titanic-dashboard
Application accessible sur : http://localhost:8501

## CI/CD — GitHub Actions
Un pipeline CI/CD est configuré avec GitHub Actions.
À chaque push sur la branche main :
Les tests unitaires sont exécutés
Si les tests réussissent :
- l’image Docker est construite
- elle est publiée sur DockerHub
Cela garantit la qualité et la reproductibilité de l’application.

## Génération d’un rapport HTML (analyse des données)
Un rapport HTML simple peut être généré à partir du dataset Titanic à l’aide de pandas et seaborn.
python generate_report.pyAfficher plus de lignes
Fichier généré : titanic-report-v1.0.html

## Monitoring et logs (ELK – démonstration)
L’application journalise les interactions utilisateurs au format JSON dans le fichier :
logs/app.log

Exemples d’événements :

pages visitées
filtres appliqués
export CSV

Une stack ELK minimale (Elasticsearch, Kibana, Filebeat) est fournie à des fins pédagogiques pour :

collecter les logs
analyser le comportement utilisateur
visualiser l’activité dans le temps

NB : Cette partie est fournie comme preuve de compréhension du monitoring DevOps (POC), et non comme une infrastructure de production complète.

## Résumé du cycle DevOps couvert

- Développement application Streamlit
- Tests unitaires
- Dockerisation
- CI/CD automatisée
- Publication de l’image Docker
- Journalisation & monitoring (ELK – démonstration)

## Auteur
Soumaya Fall
Licence 3 – Data & Intelligence Artificielle
Institut Informatique Business School (IIBS) – Sénégal