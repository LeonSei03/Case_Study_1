import streamlit as st
from devices import Device
from users import User

# Mockup
def ui_devices():
    
    if "edit_device_id" not in st.session_state:
        st.session_state.edit_device_id = None
 
    st.header("Geräte Verwaltung")

    #Icon einfügen
    st.image("Icons/add_device.png", width=80)

    # submit initialisieren
    submit = False

    # auswahl für Gerät anlegen oder ändern
    aktion = st.radio("Aktion auswählen", ["Gerät anlegen", "Gerät ändern"])

    if aktion == "Gerät anlegen":

        users = User.find_all() or []
        user_options = {f"{u.name} ({u.id})": u.id for u in users}

        with st.form("device_form"):
            device_name = st.text_input("Name des Geräts")
            device_id = st.text_input("Eindeutige ID des Geräts (Inventarnummer)")

            if users: 
                selected_label = st.selectbox("Geräteverantwortlicher Nutzer", options = list(user_options.keys()))
                responsible_person = user_options[selected_label]
            else: 
                st.warning("Es sind noch keine Nutzer angelegt")
                responsible_person = ""
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

        if search_clicked:
            device = None
            if search_id:
                device = Device.find_by_attribute("device_id", search_id)
            elif search_name:
                device = Device.find_by_attribute("device_name", search_name)

            if device:
                st.session_state.edit_device_id = device.device_id # id im edit_device_id vom sessionstate speichern (quasi unser kleiner Speicher während durchlaufen wird)
                st.info("Suchergebnis: Gerät gefunden!")
            else:
                st.session_state.edit_device_id = None
                st.error("Kein Gerät gefunden.")

        device_to_edit = None
        if st.session_state.edit_device_id: # wenn wir ne id in der sessionstate gespeicher haben
            # suche nach dem deivce mit der id aus dem sessionstate mit der Device methode find_by_attribute -> speichern in device_to_edit 
            device_to_edit = Device.find_by_attribute("device_id", st.session_state.edit_device_id) # neue instanz der Klasse 

        if device_to_edit:
            # st.info("Suchergebnis: Gerät gefunden!")
            # st.caption("Hinweis: Falls noch kein Gerät existiert, würde hier eine Fehlermeldung auftauchen.")

            with st.form("device_edit_form"):
                name = st.text_input("Name des Geräts", value=device_to_edit.device_name)
                device_id = st.text_input("Eindeutige ID des Geräts (Inventarnummer)", value=device_to_edit.device_id, disabled=True) # bzgl. disabled=True: wäre doof wenn wir die Device id
                # ändern und store_data() aber die neue id nicht findet zum abspeicehrn udn dann ein neues objekt anlegt, dann haben wir ein altes objekt noch im
                # speicher, also nicht änderbar
                responsible_person = st.text_input("Geräteverantwortlicher Nutzer", value=device_to_edit.managed_by_user_id)
                # end_of_life muss noch in die store data und __init__ aufgenommen werden. habe ich nicht gemacht weil nicht
                # weiß ob man das beim Gerät anlegen schon angeben muss
                # end_of_life = st.text_input("Datum, ab welchem das Gerät nicht mehr gewartet wird", value="01/08/2030")
                submit_edit = st.form_submit_button("Änderungen Speichern")
            
            if submit_edit:
                if name == "" or device_id == "" or responsible_person == "":
                    st.error("Bitte alle Felder ausfüllen.")
                else:
                    # neue Werte ins Device Objekt rein schreiben
                    device_to_edit.device_name = name # als kleine Erinnerung für mich:) <objekt>.<eigenschaft> = <neuer_wert>
                    device_to_edit.managed_by_user_id = responsible_person
                    device_to_edit.store_data()

                    st.success("Gerät gespeichert.")

def ui_users():
    st.header("Nutzer Verwaltung")
    st.image("Icons/user_icon.png", width=80)
    #Session-States ganz am Anfang initialisiert
    #streamlit führt bei (fast) jeder Interaktion einen "Rerun" aus...
    #Variablen, die "normal" im Code sind (z.B. edit_clicked=True) gehen verloren bei reruns ...

    if "user_search_result" not in st.session_state:
        st.session_state.user_search_result = None  #merkt sich Suchergebnis über Reruns

    if "edit_user_id" not in st.session_state:
        st.session_state.edit_user_id = None  #merkt sich, welcher Nutzer in "Alle Nutzer" gerade bearbeitet wird

    if "flash_success" not in st.session_state:
        st.session_state.flash_success = None  #Success-Message, die nach st.rerun() noch sichtbar bleiben soll

    if "flash_error" not in st.session_state:
        st.session_state.flash_error = None  #Error-Message analog

    if "flash_info" not in st.session_state:
        st.session_state.flash_info = None  #Info-Message analog

    #Problem vorher und Lösung ... 
    #setzen von st.success(...) und danach st.rerun()
    #dadurch wird der aktuelle Render "abgebrochen" und die Message ist weg
    #wir speichern die Message in session_state (flash_success/flash_error/flash_info)
    #beim nächsten Rerun wird sie oben angezeigt
    #danach löschen wir sie sofort, damit sie nur 1x erscheint

    if st.session_state.flash_success:
        st.success(st.session_state.flash_success)
        st.session_state.flash_success = None

    if st.session_state.flash_error:
        st.error(st.session_state.flash_error)
        st.session_state.flash_error = None

    if st.session_state.flash_info:
        st.info(st.session_state.flash_info)
        st.session_state.flash_info = None

    submit = False

    #Auswahl für Nutzer anlegen / anzeigen / suchen
    aktion = st.radio("Aktion auswählen", ["Nutzer anlegen", "Alle Nutzer anzeigen", "Nutzer suchen"])

    # 1) Nutzer anlegen

    if aktion == "Nutzer anlegen":
        #st.form sorgt dafür, dass Eingaben nicht bei jedem Tippen Reruns auslösen,sondern erst beim Submit
        with st.form("user_form"):
            user_name = st.text_input("Name")
            user_email = st.text_input("E-Mail-Adresse")
            submit = st.form_submit_button("Nutzer Anlegen")

        if submit:
            #strip() entfernt Leerzeichen am Anfang/Ende also weniger Eingabefehler
            if user_name.strip() == "" or user_email.strip() == "":
                st.error("Bitte Felder ausfüllen!")
            else:
                user = User(user_email, user_name)
                user.store_data()
                st.success("Nutzer gespeichert")

    # 2) Alle Nutzer anzeigen 
    if aktion == "Alle Nutzer anzeigen":
        users = User.find_all()

        if not users:
            st.info("Keine Nutzer vorhanden.")
            return

        st.subheader("Alle Nutzer")

        #Liste
        for u in users:
            col1, col2, col3, col4 = st.columns([3, 4, 2, 2])

            with col1:
                st.write(u.name)

            with col2:
                st.write(u.id)

            with col3:
                edit_clicked = st.button("Ändern", key="edit_" + u.id)
                if edit_clicked:
                    st.session_state.edit_user_id = u.id

            with col4:
                delete_clicked = st.button("Löschen", key="delete_" + u.id)
                if delete_clicked:
                    u.delete()
                    #Flash statt st.success direkt + rerun (sonst sieht man es nicht)
                    st.session_state.flash_success = f"Nutzer {u.id} gelöscht."
                    #wenn gerade derselbe Nutzer im Edit-Modus war: Edit-Modus beenden
                    if st.session_state.edit_user_id == u.id:
                        st.session_state.edit_user_id = None
                    st.rerun()

            #Edit-Block unter der Zeile NUR anzeigen, wenn dieser User ausgewählt ist
            if st.session_state.edit_user_id == u.id:
                st.info(f"Nutzer bearbeiten: {u.id}")

                # Form-Key muss eindeutig sein weil sonst vermischen von den form-states, deswegen + u.id
                with st.form("edit_form_" + u.id):
                    new_name = st.text_input("Neuer Name", value=u.name)
                    st.text_input("E-Mail-Adresse (ID)", value=u.id, disabled=True)
                    submit_row_edit = st.form_submit_button("Speichern")

                if submit_row_edit:
                    new_name = new_name.strip()
                    if new_name == "":
                        st.error("Name darf nicht leer sein.")
                    else:
                        u.name = new_name
                        u.store_data()

                        #Flash message setzen, Edit-Modus schließen, dann rerunen
                        st.session_state.flash_success = "Nutzer aktualisiert."
                        st.session_state.edit_user_id = None
                        st.rerun()

    # 3) Nutzer suchen 

    if aktion == "Nutzer suchen":
        with st.form("search_form"):
            search_email = st.text_input("Nutzer über E-Mail-Adresse suchen")
            search_name = st.text_input("Nutzer über Name suchen")
            search_clicked = st.form_submit_button("Suchen") 

        if search_clicked:
            if search_email.strip() != "":
                st.session_state.user_search_result = User.find_by_attribute("id", search_email.strip())
            elif search_name.strip() != "":
                st.session_state.user_search_result = User.find_by_attribute("name", search_name.strip())
            else:
                st.session_state.user_search_result = None

        search_result = st.session_state.user_search_result

        if search_result:
            st.info("Suchergebnis: Nutzer gefunden!")

            #erst beim Submit speichern
            with st.form("user_edit_form"):
                name = st.text_input("Name", value=search_result.name)
                email = st.text_input("E-Mail-Adresse", value=search_result.id, disabled=True)
                submit_edit = st.form_submit_button("Änderungen Speichern")

            if submit_edit:
                if name.strip() == "":
                    st.error("Name darf nicht leer sein.")
                else:
                    search_result.name = name.strip()
                    search_result.store_data()

                    st.session_state.flash_success = "Nutzer aktualisiert."
                    st.session_state.user_search_result = None
                    st.rerun()

            delete_clicked = st.button("Nutzer löschen")
            if delete_clicked:
                search_result.delete()
                st.session_state.flash_success = "Nutzer gelöscht."
                st.session_state.user_search_result = None
                st.rerun()

        elif search_clicked:
            st.warning("Kein Nutzer gefunden.")


def ui_reservations():

    st.header("Reservierungen")

    st.image("Icons/kalender_icon.png", width=80)

    st.selectbox("Gerät wählen", ["ID-1 (Lasercutter)", "ID-2 (Lasercutter)", "ID-3 (3D-Drucker)"])
    st.date_input("Startdatum")
    st.date_input("Enddatum")
    st.text_input("Projekt / Zweck")
    st.button("Reservierung eintragen")

def ui_maintenance():
        
    st.header("Wartungen")

    st.image("Icons/wartung_icon.png", width=80)

    st.selectbox("Gerät wählen", ["ID-1 (Lasercutter)", "ID-2 (Lasercutter)", "ID-3 (3D-Drucker)"])
    st.date_input("Nächster Wartungstermin")
    st.number_input("Wartungskosten pro Quartal (€)", min_value=0)
    st.button("Wartungsdaten speichern")

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


def ui():
    # Seitenüberschrift - einmal pro Seite
    #st.title("Admin")

    # Überschrift
    #st.header('Geräteverwaltung der Hochschule')

    # Seitenleiste
    auswahl = st.sidebar.radio("Menü", ["Dashboard", "Geräte-Verwaltung", "Nutzer-Verwaltung", "Reservierungs-System", "Wartungs-Management",], index=0) # 0=Dashboard, 1=Geräte-Verwaltung

    if auswahl == "Dashboard":
        ui_dashboard()
    if auswahl == "Geräte-Verwaltung":
        ui_devices()
    if auswahl == "Nutzer-Verwaltung":
        ui_users()
    if auswahl == "Reservierungs-System":
        ui_reservations()
    if auswahl == "Wartungs-Management":
        ui_maintenance()

