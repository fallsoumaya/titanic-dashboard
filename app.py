# app.py
import os
import json
import logging
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px

from data.loader import load_titanic_data


# -----------------------------
# 1) CONFIG & LOGGER JSON
# -----------------------------
st.set_page_config(page_title="Titanic Dashboard", layout="wide")

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(message)s"
)

def log_event(event_type: str, details: dict):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "details": details
    }
    logging.info(json.dumps(entry))


# -----------------------------
# 2) CHARGEMENT DATA
# -----------------------------
@st.cache_data
def get_data():
    return load_titanic_data()

df = get_data()


# -----------------------------
# 3) SIDEBAR: FILTRES GLOBAUX
# -----------------------------
st.sidebar.title("Filtres")

all_classes = sorted(df["class"].dropna().unique().tolist())
all_sexes = sorted(df["sex"].dropna().unique().tolist())
all_age_groups = df["age_group"].dropna().unique().tolist()

selected_classes = st.sidebar.multiselect("Classe", all_classes, default=all_classes)
selected_sexes = st.sidebar.multiselect("Sexe", all_sexes, default=all_sexes)
selected_age_groups = st.sidebar.multiselect("Tranche d'âge", all_age_groups, default=all_age_groups)

filtered_df = df[
    (df["class"].isin(selected_classes)) &
    (df["sex"].isin(selected_sexes)) &
    (df["age_group"].isin(selected_age_groups))
].copy()

log_event("filters_applied", {
    "class": selected_classes,
    "sex": selected_sexes,
    "age_group": [str(x) for x in selected_age_groups],
    "rows_after_filter": int(len(filtered_df))
})


# -----------------------------
# 4) NAVIGATION: 4 PAGES (NOMS DU SUJET)
# -----------------------------
st.title("Titanic Dashboard (Projet DevOps)")

PAGES = [
    "Vue générale",
    "Analyse de survie",
    "Filtres interactifs",
    "Données brutes"
]

page = st.sidebar.radio("Pages", PAGES)

log_event("page_visited", {"page": page})


# =========================================================
# PAGE 1 — VUE GÉNÉRALE
# =========================================================
def page_vue_generale(data: pd.DataFrame):
    st.header("Vue générale")

    # KPI demandés : nombre passagers, taux survie, âge moyen
    col1, col2, col3 = st.columns(3)

    nb_passagers = len(data)
    taux_survie = round(data["survived"].mean() * 100, 2) if nb_passagers > 0 else 0
    age_moyen = round(data["age"].mean(), 1) if nb_passagers > 0 else 0

    col1.metric("Nombre de passagers", nb_passagers)
    col2.metric("Taux de survie global (%)", taux_survie)
    col3.metric("Âge moyen", age_moyen)

    st.subheader("Aperçu (après filtres)")
    st.dataframe(data.head(30), use_container_width=True)


# =========================================================
# PAGE 2 — ANALYSE DE SURVIE
# =========================================================
def page_analyse_survie(data: pd.DataFrame):
    st.header("Analyse de survie")

    if len(data) == 0:
        st.warning("Aucune donnée avec ces filtres. Modifie les filtres dans la sidebar.")
        return

    # 1) Survie par sexe (bar chart)
    st.subheader("Taux de survie par sexe")
    sex_survival = data.groupby("sex", as_index=False)["survived"].mean()
    sex_survival["survived"] = sex_survival["survived"] * 100

    fig_sex = px.bar(
        sex_survival,
        x="sex",
        y="survived",
        color="sex",
        labels={"sex": "Sexe", "survived": "Taux de survie (%)"},
        text="survived"
    )
    fig_sex.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig_sex, use_container_width=True)

    # 2) Survie par classe (pie chart)
    st.subheader("Survie par classe (répartition des survivants)")
    survivors = data[data["survived"] == 1]
    if len(survivors) == 0:
        st.info("Aucun survivant avec ces filtres.")
    else:
        class_counts = survivors["class"].value_counts().reset_index()
        class_counts.columns = ["class", "count"]

        fig_class = px.pie(
            class_counts,
            names="class",
            values="count",
            labels={"class": "Classe", "count": "Nombre de survivants"}
        )
        st.plotly_chart(fig_class, use_container_width=True)

    # 3) Survie par tranche d'âge (histogram)
    st.subheader("Survie par tranche d'âge")
    fig_age = px.histogram(
        data,
        x="age_group",
        color="survived",
        barmode="group",
        labels={"age_group": "Tranche d'âge", "survived": "Survécu (0/1)"},
    )
    st.plotly_chart(fig_age, use_container_width=True)


# =========================================================
# PAGE 3 — FILTRES INTERACTIFS
# (Page dédiée pour montrer le filtrage + résumé)
# =========================================================
def page_filtres_interactifs(data: pd.DataFrame):
    st.header("Filtres interactifs")

    st.markdown("Cette page montre clairement l'impact des filtres sur les données et les indicateurs.")

    colA, colB = st.columns(2)

    with colA:
        st.subheader("Résumé des filtres actuels")
        st.write("**Classe :**", ", ".join(selected_classes) if selected_classes else "Aucune")
        st.write("**Sexe :**", ", ".join(selected_sexes) if selected_sexes else "Aucun")
        st.write("**Tranche d'âge :**", ", ".join([str(x) for x in selected_age_groups]) if selected_age_groups else "Aucune")

        st.info(f"Lignes après filtrage : **{len(data)}**")

    with colB:
        st.subheader("Répartition (après filtres)")
        if len(data) == 0:
            st.warning("Aucune donnée avec ces filtres.")
        else:
            fig = px.histogram(data, x="class", color="sex", barmode="group",
                               labels={"class": "Classe", "sex": "Sexe"})
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Aperçu des données filtrées")
    st.dataframe(data, use_container_width=True)


# =========================================================
# PAGE 4 — DONNÉES BRUTES + EXPORT CSV
# =========================================================
def page_donnees_brutes(data: pd.DataFrame):
    st.header("Données brutes")

    if len(data) == 0:
        st.warning("Aucune donnée à afficher avec ces filtres.")
        return

    st.dataframe(data, use_container_width=True)

    csv = data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Exporter en CSV",
        data=csv,
        file_name="titanic_filtered.csv",
        mime="text/csv"
    )

    log_event("csv_export_available", {"rows": int(len(data))})


# -----------------------------
# 5) ROUTEUR: AFFICHER LA PAGE
# -----------------------------
if page == "Vue générale":
    page_vue_generale(filtered_df)
elif page == "Analyse de survie":
    page_analyse_survie(filtered_df)
elif page == "Filtres interactifs":
    page_filtres_interactifs(filtered_df)
elif page == "Données brutes":
    page_donnees_brutes(filtered_df)