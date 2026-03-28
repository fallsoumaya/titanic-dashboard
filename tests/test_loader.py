import pandas as pd
from data.loader import load_titanic_data

# Colonnes minimales attendues pour ton dashboard
REQUIRED_COLUMNS = {"survived", "sex", "class", "age", "age_group"}

def test_loader_returns_dataframe():
    df = load_titanic_data()
    assert isinstance(df, pd.DataFrame), "Le loader doit retourner un DataFrame pandas."

def test_dataframe_not_empty():
    df = load_titanic_data()
    assert len(df) > 0, "Le DataFrame ne doit pas être vide."

def test_required_columns_exist():
    df = load_titanic_data()
    missing = REQUIRED_COLUMNS - set(df.columns)
    assert len(missing) == 0, f"Colonnes manquantes : {missing}"

def test_no_nulls_in_critical_columns():
    df = load_titanic_data()
    # Le sujet impose de gérer les valeurs nulles ; ici on vérifie les colonnes critiques
    assert df["age"].isna().sum() == 0, "La colonne age ne doit pas contenir de valeurs nulles."
    assert df["sex"].isna().sum() == 0, "La colonne sex ne doit pas contenir de valeurs nulles."
    assert df["class"].isna().sum() == 0, "La colonne class ne doit pas contenir de valeurs nulles."
    assert df["survived"].isna().sum() == 0, "La colonne survived ne doit pas contenir de valeurs nulles."

def test_survived_is_binary():
    df = load_titanic_data()
    values = set(df["survived"].unique().tolist())
    assert values.issubset({0, 1}), f"survived doit contenir seulement 0/1, trouvé : {values}"