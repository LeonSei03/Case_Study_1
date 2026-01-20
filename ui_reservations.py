import streamlit as st

def ui_reservations():

    st.header("Reservierungen")

    st.image("Icons/kalender_icon.png", width=80)

    st.selectbox("Gerät wählen", ["ID-1 (Lasercutter)", "ID-2 (Lasercutter)", "ID-3 (3D-Drucker)"])
    st.date_input("Startdatum")
    st.date_input("Enddatum")
    st.text_input("Projekt / Zweck")
    st.button("Reservierung eintragen")