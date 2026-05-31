import streamlit as st
import pandas as pd
from utils import load_movies

st.title("Analiza podatkov")

movies = load_movies()

st.sidebar.header("Filtri")
min_review_count = st.sidebar.slider("Minimalno število ocen", min_value=0, max_value=int(movies["Review Count"].max()), value=0)
genres = st.sidebar.multiselect("Izberite žanre", options=sorted(movies["Genres split"].explode().dropna().unique()))
year = st.sidebar.multiselect("Izberite leto", options=sorted(movies["year"].unique()), max_selections=1)

filtered = movies.copy()
if genres:
    filtered = filtered[filtered["Genres split"].apply(lambda x: any(g in x for g in genres))]
filtered = filtered[filtered["Review Count"] >= min_review_count]
if year:
    filtered = filtered[filtered["year"] == year[0]]

st.markdown("### Top 10 filmov po povprečni oceni")
st.dataframe(filtered[["title", "genres", "Review Count", "Average Rating"]].sort_values(by="Average Rating", ascending=False).head(10))

st.markdown("### Kratek povzetek")
col1, col2 = st.columns(2)
with col1:
    st.metric("Število filmov (po filtrih)", int(filtered.shape[0]))
with col2:
    st.metric("Najvišja povprečna ocena", round(filtered["Average Rating"].max(), 2) if not filtered.empty else "-")
