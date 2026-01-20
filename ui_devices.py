import streamlit as st
from devices import Device
from users import User
import session_states


def ui_devices():
    
    st.header("Geräte Verwaltung")

    #Icon einfügen
    st.image("Icons/add_device.png", width=80)

    # submit initialisieren
    submit = False

    # auswahl für Gerät anlegen oder ändern
    aktion = st.radio("Aktion auswählen", ["Gerät anlegen", "Geräte anzeigen", "Gerät ändern"])

    if aktion != "Geräte anzeigen":
        st.session_state["edit_device_id"] = None

    if aktion == "Geräte anzeigen":
        devices = Device.find_all()

        if not devices:
            st.info("Kein Gerät vorhanden.")
            return

        st.subheader("Alle Geräte")

        for d in devices:
            col1, col2, col3, col4 = st.columns([3, 4, 2, 2])

            with col1:
                st.write(d.device_name)

            with col2:
                st.write(d.id)

            with col3:
                if st.button("Ändern", key=f"edit_{d.id}"):
                    st.session_state["edit_device_id"] = d.id

            with col4:
                if st.button("Löschen", key=f"delete_{d.id}"):
                    d.delete()
                    session_states.flash(f"Gerät {d.id} gelöscht.")
                    if st.session_state["edit_device_id"] == d.id:
                        st.session_state["edit_device_id"] = None
                    st.rerun()

            if st.session_state["edit_device_id"] == d.id:
                st.info(f"Gerät bearbeiten: {d.id}")

                with st.form(f"edit_form_{d.id}"):
                    new_device = st.text_input("Neuer Gerätename", value=d.device_name)
                    st.text_input("Geräte ID", value=d.id, disabled=True)
                    submit_row_edit = st.form_submit_button("Speichern")

                if submit_row_edit:
                    new_device = new_device.strip()
                    if new_device == "":
                        st.error("Name darf nicht leer sein.")
                    else:
                        d.device_name = new_device
                        d.store_data()
                        session_states.flash("Gerät aktualisiert.")
                        st.session_state["edit_device_id"] = None
                        st.rerun()

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
                session_states.flash("Gerät gespeichert")
                st.rerun()

    if aktion == "Gerät ändern":

        devices = Device.find_all()

        if not devices:
            st.info("Kein Gerät vorhanden.")
            return
        
        st.subheader("Gerät suchen")
        search_id = st.text_input("Gerät suchen mit dessen ID (bzw. Inventarnummer)")
        search_name = st.text_input("Gerät suchen mit dessen Namen:")
        search_clicked = st.button("Suchen")

        if search_clicked:
            device = None
            if search_id:
                device = Device.find_by_attribute("id", search_id)
            elif search_name:
                device = Device.find_by_attribute("device_name", search_name)

            if device:
                st.session_state["edit_device_id"] = device.id # id im edit_device_id vom sessionstate speichern (quasi unser kleiner Speicher während durchlaufen wird)
                st.info("Suchergebnis: Gerät gefunden!")
            else:
                st.session_state["edit_device_id"] = None
                st.error("Kein Gerät gefunden.")

        device_to_edit = None
        if st.session_state["edit_device_id"]: # wenn wir ne id in der sessionstate gespeicher haben
            # suche nach dem deivce mit der id aus dem sessionstate mit der Device methode find_by_attribute -> speichern in device_to_edit 
            device_to_edit = Device.find_by_attribute("id", st.session_state["edit_device_id"]) # neue instanz der Klasse 

        if device_to_edit:
            # st.info("Suchergebnis: Gerät gefunden!")
            # st.caption("Hinweis: Falls noch kein Gerät existiert, würde hier eine Fehlermeldung auftauchen.")
            with st.form("device_edit_form"):
                name = st.text_input("Name des Geräts", value=device_to_edit.device_name)
                device_id = st.text_input("Eindeutige ID des Geräts (Inventarnummer)", value=device_to_edit.id, disabled=True) # bzgl. disabled=True: wäre doof wenn wir die Device id
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