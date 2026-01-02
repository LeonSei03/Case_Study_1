import streamlit as st
from devices import Device

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
            device_name = st.text_input("Name des Geräts")
            device_id = st.text_input("Eindeutige ID des Geräts (Inventarnummer)")
            responsible_person = st.text_input("Geräteverantwortlicher Nutzer")
            # end_of_life = st.text_input("Datum, ab welchem das Gerät nicht mehr gewartet wird")
            #__last_update = st.text_input("Inventarnummer-ID")
            #__creation_date = st.text_input("Inventarnummer-ID")
            submit = st.form_submit_button("Speichern") # bestätigungsbutton
    
    if submit:
        if device_name == "" or device_id == "" or responsible_person == "":
            st.error("Bitte alle Felder ausfüllen.")
        else:
            # Device Objekt erstellen (ging vorher nicht, weil das keine Klassenmethode war,
            # sondern eine Instanzmethode, also kann man nur auf Objekte der Klasse anwenden,
            # deswegen erst ein KlassenObjekt erstellen)
            device = Device(device_name, device_id, responsible_person)
            device.store_data() # in die DB schreiben
            st.success("Gerät gespeichert.")
            

    if aktion == "Gerät ändern":
        st.subheader("Gerät suchen")
        search_id = st.text_input("Gerät suchen mit dessen ID (bzw. Inventarnummer)")
        search_name = st.text_input("Gerät suchen mit dessen Namen:")
        search_clicked = st.button("Suchen")

        search_result = None

        if search_clicked:
            if search_id:
                search_result = Device.find_by_attribute("device_id", search_id)
            elif search_name:
                search_result = Device.find_by_attribute("device_name", search_name)
                search_result = Device.find_by_attribute(search_id, search_name)

        if search_clicked and search_result:
            st.info("Suchergebnis: Gerät gefunden!")
            # st.caption("Hinweis: Falls noch kein Gerät existiert, würde hier eine Fehlermeldung auftauchen.")

            with st.form("device_edit_form"):
                name = st.text_input("Name des Geräts", value=search_result.device_name)
                device_id = st.text_input("Eindeutige ID des Geräts (Inventarnummer)", value=search_result.device_id, disabled=True) # bzgl. disabled=True: wäre doof wenn wir die Device id
                # ändern und store_data() aber die neue id nicht findet zum abspeicehrn udn dann ein neues objekt anlegt, dann haben wir ein altes objekt noch im
                # speicher, also nicht änderbar
                responsible_person = st.text_input("Geräteverantwortlicher Nutzer", value=search_result.managed_by_user_id)
                # end_of_life muss noch in die store data und __init__ aufgenommen werden. habe ich nicht gemacht weil nicht
                # weiß ob man das beim Gerät anlegen schon angeben muss
                # end_of_life = st.text_input("Datum, ab welchem das Gerät nicht mehr gewartet wird", value="01/08/2030")
                submit_edit = st.form_submit_button("Änderungen Speichern")
            
            
            if submit_edit:
                if name == "" or device_id == "" or responsible_person == "":
                    st.error("Bitte alle Felder ausfüllen.")
                else:
                    # neue Werte ins Device Objekt rein schreiben
                    search_result.device_name = name
                    search_result.device_id = device_id
                    search_result.managed_by_user_id = responsible_person

                    search_result.store_data()
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

