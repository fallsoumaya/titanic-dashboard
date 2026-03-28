# Titanic Dashboard (Streamlit) — Projet DevOps

Application Streamlit interactive basée sur le dataset Titanic (seaborn).

## Lancer l'app
pip install -r requirements.txt  
streamlit run app.py

## Lancer les tests
pytest -v

## Fonctionnalités
- 4 pages : Vue générale, Analyse de survie, Filtres interactifs, Données brutes
- Filtres (classe, sexe, tranche d'âge)
- Logs JSON dans logs/app.log (pour ELK)
- Export CSV