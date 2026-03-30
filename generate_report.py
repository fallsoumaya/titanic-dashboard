import pandas as pd
import seaborn as sns

# Charger les données Titanic
df = sns.load_dataset("titanic")

# Statistiques descriptives
summary = df.describe(include="all")

# Générer un fichier HTML simple
with open("titanic-report-v1.0.html", "w", encoding="utf-8") as f:
    f.write("<html><head><title>Titanic Report</title></head><body>")
    f.write("<h1>Rapport d'analyse du dataset Titanic</h1>")
    f.write("<h2>Aperçu des données</h2>")
    f.write(df.head(20).to_html())
    f.write("<h2>Statistiques descriptives</h2>")
    f.write(summary.to_html())
    f.write("</body></html>")