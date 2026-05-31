import streamlit as st

st.title("Izberi stran")

if st.button("Analiza podatkov"):
    st.switch_page("pages/0_Analiza_podatkov.py")

if st.button("Primerjava"):
    st.switch_page("pages/1_Primerjava_filmov.py")

if st.button("Priporočila"):
    st.switch_page("pages/2_Priporočila.py")
