import streamlit as st
import seaborn as sns
import pandas as pd

st.set_page_config(page_title="Titanic Dashboard", layout="wide")

st.title("🚢 Titanic Dashboard")

@st.cache_data
def load_data():
    df = sns.load_dataset("titanic")
    return df

df = load_data()

st.metric("👥 Passagers", len(df))
st.metric("✅ Taux de survie", round(df["survived"].mean() * 100, 2))
st.metric("🎂 Âge moyen", round(df["age"].mean(), 1))

st.subheader("Aperçu des données")
st.dataframe(df.head(20))