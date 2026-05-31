import numpy as np
import pandas as pd
import streamlit as st

import warnings
warnings.filterwarnings('ignore')

_CACHE_DATA = "data/prepared_data.parquet"
_CACHE_MOVIES = "data/movies.parquet"

def _prepare_data():
    ratings = pd.read_csv("data/ratings.csv")
    X = ratings.pivot_table(index="movieId", columns="userId", values="rating")
    X.dropna(how='all', inplace=True)
    X.fillna(0, inplace=True)
    X.to_parquet(_CACHE_DATA, index=False)
    return X

def _prepare_movies():
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")

    movies["Review Count"] = ratings.groupby('movieId')['rating'].count()
    movies["Average Rating"] = ratings.groupby('movieId')['rating'].mean()

    movies["Genres split"] = movies["genres"].str.split("|")

    movies["year"] = movies["title"].str.extract(r"\((\d{4})\)").astype(float)
    movies["year"] = movies["year"].fillna(0).astype(int).astype(str).replace("0", "Unknown")

    movies.to_parquet(_CACHE_MOVIES, index=False)
    return movies

#@st.cache_data
def load_data():
    try:
        return pd.read_parquet(_CACHE_DATA)
    except FileNotFoundError:
        return _prepare_data()

#@st.cache_data
def load_movies():
    try:
        return pd.read_parquet(_CACHE_MOVIES)
    except FileNotFoundError:
        return _prepare_movies()
