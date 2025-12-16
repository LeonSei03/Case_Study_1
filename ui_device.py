import streamlit as st
#from queries import find_devices
#from devices import Device

# Mockup
def ui():
    # Seitenüberschrift - einmal pro Seite
    st.title("Admin")

    # Überschrift
    st.header('Geräteverwaltung der Hochschule')

    # Seitenleiste
    auswahl = st.sidebar.radio("Menü", ["Dashboard", "Geräte-Verwaltung", "Nutzer-Verwaltung", "Reservierungs-System", "Wartungs-Management",], index=1) # 0=Dashboard, 1=Geräte-Verwaltung

    # submit initialisieren
    submit = False

    # alles zu Geräte Verwaltung kommt in die if
    if auswahl == "Geräte-Verwaltung":
        st.write("Hier ist die Geräteverwaltung")

        # auswahl für Gerät anlegen oder ändern
        aktion = st.radio("Aktion auswählen", ["Gerät anlegen", "Gerät ändern"])

        if aktion == "Gerät anlegen":
            with st.form("device_form"):
                name = st.text_input("Name des Geräts")
                id = st.text_input("Eindeutige ID des Geräts (Inventarnummer)")
                responsible_person = st.text_input("Geräteverantwortlicher Nutzer")
                end_of_life = st.text_input("Datum, ab welchem das Gerät nicht mehr gewartet wird")
                #__last_update = st.text_input("Inventarnummer-ID")
                #__creation_date = st.text_input("Inventarnummer-ID")
                submit = st.form_submit_button("Speichern") # bestätigungsbutton
        
        if submit:
            if name == "" or id == "":
                st.error("Bitte alle Pflichtfelder ausfüllen.")
            else:
                st.success("Gerät gespeichert.")

    if auswahl == "Nutzer-Verwaltung":
        st.write("Hier ist die Nutzer-Verwaltung")

            # auswahl für Gerät anlegen oder ändern
        aktion = st.radio("Aktion auswählen", ["Nutzer anlegen", "Nutzer suchen"])

        if aktion == "Nutzer anlegen":
            st.text_input("Name")
            st.text_input("E-Mail-Adresse")
            st.button("Nutzer anlegen")

        if aktion == "Nutzer suchen":
            st.text_input("Name oder E-Mail-Adresse eingeben")
            st.button("Nutzer suchen")


    if auswahl == "Reservierungs-System":
        st.write("Hier ist das Reservierungs-System")

        st.selectbox("Gerät", ["3D-Drucker", "Laser-Cutter", "CNC-Fräse"])
        st.date_input("Startdatum")
        st.date_input("Enddatum")
        st.text_input("Projekt / Zweck")
        st.button("Reservierung eintragen")


    if auswahl == "Wartungs-Management":
        st.write("Hier ist das Wartungs-Management")

        st.selectbox("Gerät", ["3D-Drucker", "Laser-Cutter", "CNC-Fräse"])
        st.date_input("Nächster Wartungstermin")
        st.number_input("Wartungskosten pro Quartal (€)", min_value=0)
        st.button("Wartungsdaten speichern")


if False: 
    '''
    # Eine Überschrift der ersten Ebene
    st.write("# Gerätemanagement")

    # Eine Überschrift der zweiten Ebene
    st.write("## Geräteauswahl")

    # Eine Auswahlbox mit Datenbankabfrage, das Ergebnis wird in current_device gespeichert
    devices_in_db = find_devices()

    if devices_in_db:
        current_device_name = st.selectbox(
            'Gerät auswählen',
            options=devices_in_db, key="sbDevice")

        if current_device_name in devices_in_db:
            loaded_device = Device.find_by_attribute("device_name", current_device_name)
            if loaded_device:
                st.write(f"Loaded Device: {loaded_device}")
            else:
                st.error("Device not found in the database.")

            with st.form("Device"):
                st.write(loaded_device.device_name)

                text_input_val = st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id)
                loaded_device.set_managed_by_user_id(text_input_val)

                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                if submitted:
                    loaded_device.store_data()
                    st.write("Data stored.")
                    st.rerun()
        else:
            st.error("Selected device is not in the database.")
    else:
        st.write("No devices found.")
        st.stop()

    st.write("Session State:")
    st.session_state
    '''
