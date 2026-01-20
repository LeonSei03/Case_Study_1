import streamlit as st 
from users import User
from devices import Device 

def ui_dashboard():

    st.header("Dashboard")

    # Daten einmal aus der Datenbank holen
    users = User.find_all()
    devices = Device.find_all()

    # Falls None zurückkommt, sicherheitshalber auf 0 setzen
    user_count = len(users) if users else 0
    device_count = len(devices) if devices else 0

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Anzahl Nutzer", value=user_count)

    with col2:
        st.metric(label="Anzahl Geräte", value=device_count)