# data/loader.py
import pandas as pd
import seaborn as sns


EXPECTED_COLUMNS = {
    "survived", "pclass", "sex", "age", "sibsp", "parch",
    "fare", "embarked", "class", "who", "adult_male", "deck", "embark_town", "alive", "alone"
}


def load_titanic_data() -> pd.DataFrame:
    """
    Charge le dataset Titanic depuis seaborn et effectue un nettoyage minimal.
    Retourne un DataFrame prêt à être utilisé dans Streamlit.
    """
    df = sns.load_dataset("titanic")

    # Nettoyage minimal: on garde les lignes nécessaires aux graphiques principaux
    df = df.copy()
    df = df.dropna(subset=["survived", "sex", "class", "age"])

    # Sécurisation types
    df["survived"] = df["survived"].astype(int)

    # Tranches d'âge (demandé par le sujet: survie par tranche d'âge)
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 12, 18, 35, 60, 120],
        labels=["Enfant (0-12)", "Ado (13-18)", "Adulte (19-35)", "Senior (36-60)", "Âgé (60+)"],
        include_lowest=True
    )

    return df