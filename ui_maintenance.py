import streamlit as st 


def ui_maintenance():
        
    st.header("Wartungen")

    st.image("Icons/wartung_icon.png", width=80)

    st.selectbox("Gerät wählen", ["ID-1 (Lasercutter)", "ID-2 (Lasercutter)", "ID-3 (3D-Drucker)"])
    st.date_input("Nächster Wartungstermin")
    st.number_input("Wartungskosten pro Quartal (€)", min_value=0)
    st.button("Wartungsdaten speichern")