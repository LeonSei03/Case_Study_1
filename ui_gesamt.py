import streamlit as st
import ui_devices
import ui_users
import session_states
import ui_dashboard
import ui_maintenance
import ui_reservations


def ui():
    session_states.session_states()
    session_states.flash_anzeigen() #bei jedem rerun werden die messages angezeigt wenn was erstellt oder gelöscht wurde 

   # Seitenleiste
    auswahl = st.sidebar.radio("Menü", ["Dashboard", "Geräte-Verwaltung", "Nutzer-Verwaltung", "Reservierungs-System", "Wartungs-Management",], index=0) # 0=Dashboard, 1=Geräte-Verwaltung

    if auswahl == "Dashboard":
        ui_dashboard.ui_dashboard()
    if auswahl == "Geräte-Verwaltung":
        ui_devices.ui_devices()
    if auswahl == "Nutzer-Verwaltung":
        ui_users.ui_users()
    if auswahl == "Reservierungs-System":
        ui_reservations.ui_reservations()
    if auswahl == "Wartungs-Management":
        ui_maintenance.ui_maintenance()








