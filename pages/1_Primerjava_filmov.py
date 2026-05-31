import streamlit as st
import pandas as pd
import altair as alt
from utils import load_movies

st.title("Primerjava filmov")

movies = load_movies()

st.markdown("Izberite dva filma za primerjavo statistik in grafov.")
movie_titles = movies["title"].tolist()
col1, col2 = st.columns(2)
with col1:
    film_a = st.selectbox("Film A", options=movie_titles, index=0)
with col2:
    film_b = st.selectbox("Film B", options=movie_titles, index=1)

ratings = pd.read_csv("data/ratings.csv")
ratings["ts"] = pd.to_datetime(ratings["timestamp"], unit='s')
ratings["year"] = ratings["ts"].dt.year

def stats_for(title):
    mid = movies.loc[movies["title"] == title, "movieId"].iloc[0]
    r = ratings[ratings["movieId"] == mid]
    return {
        "mean": r["rating"].mean(),
        "count": r["rating"].count(),
        "std": r["rating"].std(),
        "hist": r["rating"].value_counts().sort_index(),
        "year_avg": r.groupby("year")["rating"].mean().reset_index(name="avg"),
        "year_count": r.groupby("year")["rating"].count().reset_index(name="count")
    }

st.markdown("## Statistika ocen")
sa = stats_for(film_a)
sb = stats_for(film_b)

col1, col2 = st.columns(2)
with col1:
    st.subheader(film_a)
    st.metric("Povprečna ocena", round(sa["mean"], 2) if sa["count"]>0 else "-", delta=None)
    st.metric("Število ocen", int(sa["count"]))
    st.metric("Standardni odklon", round(sa["std"], 2) if pd.notna(sa["std"]) else "-")
with col2:
    st.subheader(film_b)
    st.metric("Povprečna ocena", round(sb["mean"], 2) if sb["count"]>0 else "-", delta=None)
    st.metric("Število ocen", int(sb["count"]))
    st.metric("Standardni odklon", round(sb["std"], 2) if pd.notna(sb["std"]) else "-")

st.markdown("## Histogram ocen")
ha = sa["hist"].reindex([1,2,3,4,5]).fillna(0).reset_index()
hchart_a = alt.Chart(ha).mark_bar().encode(x=alt.X('index:O', title='Ocena'), y=alt.Y('rating:Q', title='Število'))
st.subheader(film_a)
st.altair_chart(hchart_a, use_container_width=True)

hb = sb["hist"].reindex([1,2,3,4,5]).fillna(0).reset_index()
hchart_b = alt.Chart(hb).mark_bar(color="orange").encode(x=alt.X('index:O', title='Ocena'), y=alt.Y('rating:Q', title='Število'))
st.subheader(film_b)
st.altair_chart(hchart_b, use_container_width=True)

st.markdown("## Povprečna ocena po letih")
ya = sa["year_avg"]
yb = sb["year_avg"]
if not ya.empty or not yb.empty:
    ya["film"] = film_a
    yb["film"] = film_b
    df_year = pd.concat([ya, yb], ignore_index=True)
    line = alt.Chart(df_year).mark_line(point=True).encode(x='year:O', y='avg:Q', color='film:N')
    st.altair_chart(line, use_container_width=True)

st.markdown("## Število ocen po letih")
ca = sa["year_count"]
cb = sb["year_count"]
if not ca.empty or not cb.empty:
    ca["film"] = film_a
    cb["film"] = film_b
    df_count = pd.concat([ca, cb], ignore_index=True)
    bar = alt.Chart(df_count).mark_bar().encode(x='year:O', y='count:Q', color='film:N')
    st.altair_chart(bar, use_container_width=True)