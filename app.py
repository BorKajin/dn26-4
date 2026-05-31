import streamlit as st

st.title("Movie Recommender System")
st.markdown(
    "Dobrodošli v aplikaciji za analizo filmov in priporočila. Uporabite spodnje povezave ali ikono **Pages** v stranski vrstici za dostop do vseh strani."
)

st.markdown("### Povezave do razpoložljivih strani")
st.markdown(
    "- [Analiza podatkov](?page=0_Analiza_podatkov)\n"
    "- [Primerjava filmov](?page=1_Primerjava_filmov)\n"
    "- [Priporočila](?page=2_Priporocila)"
)

st.info(
    "Opomba: Če se povezave ne odprejo, izberite stran v stranski vrstici **Pages**."
)
