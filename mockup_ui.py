import streamlit as st

# Mockup    
def ui_devices():
 
    st.write("Hier ist die Geräteverwaltung")

    #Icon einfügen 
    st.image("Icons/add_device.png", width=80)

    # submit initialisieren
    submit = False

    # auswahl für Gerät anlegen oder ändern
    aktion = st.radio("Aktion auswählen", ["Gerät anlegen", "Gerät ändern"])

    if aktion == "Gerät anlegen":
        with st.form("device_form"):
            name = st.text_input("Name des Geräts")
            device_id = st.text_input("Eindeutige ID des Geräts (Inventarnummer)")
            responsible_person = st.text_input("Geräteverantwortlicher Nutzer")
            end_of_life = st.text_input("Datum, ab welchem das Gerät nicht mehr gewartet wird")
            #__last_update = st.text_input("Inventarnummer-ID")
            #__creation_date = st.text_input("Inventarnummer-ID")
            submit = st.form_submit_button("Speichern") # bestätigungsbutton
    
    if submit:
        if name == "" or device_id == "":
            st.error("Bitte alle Pflichtfelder ausfüllen.")
        else:
            st.success("Gerät gespeichert.")

def ui_users():

    st.write("Hier ist die Nutzer-Verwaltung")

    st.image("Icons/user_icon.png", width=80)

        # auswahl für Gerät anlegen oder ändern
    aktion = st.radio("Aktion auswählen", ["Nutzer anlegen", "Nutzer suchen"])

    if aktion == "Nutzer anlegen":
        st.text_input("Name")
        st.text_input("E-Mail-Adresse")
        st.button("Nutzer anlegen")

    if aktion == "Nutzer suchen":
        st.text_input("Name oder E-Mail-Adresse eingeben")
        st.button("Nutzer suchen")

def ui_reservations():

    st.write("Hier ist das Reservierungs-System")

    st.image("Icons/kalender_icon.png", width=80)

    st.selectbox("Gerät wählen", ["ID-1 (Lasercutter)", "ID-2 (Lasercutter)", "ID-3 (3D-Drucker)"])
    st.date_input("Startdatum")
    st.date_input("Enddatum")
    st.text_input("Projekt / Zweck")
    st.button("Reservierung eintragen")

def ui_maintenance():
        
    st.write("Hier ist das Wartungs-Management")

    st.image("Icons/wartung_icon.png", width=80)

    st.selectbox("Gerät wählen", ["ID-1 (Lasercutter)", "ID-2 (Lasercutter)", "ID-3 (3D-Drucker)"])
    st.date_input("Nächster Wartungstermin")
    st.number_input("Wartungskosten pro Quartal (€)", min_value=0)
    st.button("Wartungsdaten speichern")

def ui():
    # Seitenüberschrift - einmal pro Seite
    st.title("Admin")

    # Überschrift
    st.header('Geräteverwaltung der Hochschule')

    # Seitenleiste
    auswahl = st.sidebar.radio("Menü", ["Dashboard", "Geräte-Verwaltung", "Nutzer-Verwaltung", "Reservierungs-System", "Wartungs-Management",], index=1) # 0=Dashboard, 1=Geräte-Verwaltung

    if auswahl == "Dashboard":
        st.write("Dashboard")
    if auswahl == "Geräte-Verwaltung":
        ui_devices()
    if auswahl == "Nutzer-Verwaltung":
        ui_users()
    if auswahl == "Reservierungs-System":
        ui_reservations()
    if auswahl == "Wartungs-Management":
        ui_maintenance()

