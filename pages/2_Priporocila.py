import streamlit as st
import pandas as pd
import numpy as np
from utils import load_movies, load_data
from sklearn.linear_model import Lasso


st.title("Priporočilni sistem (preprosta različica)")

if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'user_ratings' not in st.session_state:
    st.session_state['user_ratings'] = {}

with st.sidebar.form("auth"):
    username = st.text_input("Uporabniško ime")
    login = st.form_submit_button("Prijava / Registracija")
    if login and username:
        st.session_state['user'] = username

if st.session_state['user'] is None:
    st.info("Prijavite se v levi stranski vrstici, da ocenjujete filme.")
    st.stop()

st.write(f"Prijavljen: **{st.session_state['user']}**")

movies = load_movies()
title_to_id = dict(zip(movies['title'], movies['movieId']))

st.markdown("### Ocenite film")
col1, col2 = st.columns([3,1])
with col1:
    sel = st.selectbox("Izberite film", options=movies['title'].tolist())
with col2:
    r = st.slider("Ocena", min_value=1, max_value=5, value=4)

if st.button("Dodaj oceno"):
    mid = int(title_to_id[sel])
    st.session_state['user_ratings'][mid] = r
    st.success(f"Dodano: {sel} = {r}")

st.markdown("### Vaše ocene (trenutno)")
if st.session_state['user_ratings']:
    df = pd.DataFrame([
        {"movieId": k, "title": movies.loc[movies['movieId']==k,'title'].iloc[0], "rating": v}
        for k,v in st.session_state['user_ratings'].items()
    ])
    st.dataframe(df)
else:
    st.write("Nimate še ocen.")

st.markdown("### Priporočila")
if len(st.session_state['user_ratings']) < 10:
    st.info("Vnesite vsaj 10 ocen, da dobite priporočila.")
else:
    rated_ids = set(st.session_state['user_ratings'].keys())
    X = load_data()
    ratings = pd.read_csv("data/ratings.csv")
    movie_ids = sorted(ratings["movieId"].unique())

    Xnovi = pd.DataFrame(index=X.index)
    Xnovi[0] = 0
    for mid, r in st.session_state['user_ratings'].items():
        if mid in movie_ids:
            Xnovi.at[movie_ids.index(mid), 0] = r

    y = Xnovi[0].values
    X_Features = X.values

    pomembni = np.nonzero(y)[0]
    if len(pomembni) == 0:
        st.error("Vaših ocen ni mogoče uvoziti v model. Prosim, ocenite filme, ki imajo ocene v zbirki.")
    else:
        y_pomembni = y[pomembni]
        X_pomembni = X_Features[pomembni, :]
        model = Lasso(alpha=0.08, max_iter=5000)
        model.fit(X_pomembni, y_pomembni)

        X_pred = model.predict(X_Features)
        recommendation_df = pd.DataFrame({
            "movieId": movie_ids,
            "predicted_rating": X_pred
        })
        recommendation_df = recommendation_df[~recommendation_df["movieId"].isin(rated_ids)]

        top10 = recommendation_df.nlargest(10, "predicted_rating")
        top10 = top10.merge(
            movies[["movieId", "title", "genres", "Review Count", "Average Rating"]],
            on="movieId",
            how="left"
        )
        top10 = top10[["title", "genres", "Review Count", "Average Rating", "predicted_rating"]]
        top10.columns = ["Naslov", "Žanri", "Število ocen", "Povprečna ocena", "Napovedana ocena"]

        st.markdown("#### 10 priporočil za vas")
        st.dataframe(top10.style.format({"Napovedana ocena": "{:.2f}", "Povprečna ocena": "{:.2f}"}))


    