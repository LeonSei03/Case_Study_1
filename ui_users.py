import streamlit as st
from users import User
import session_states

def ui_users():
    st.header("Nutzer Verwaltung")
    st.image("Icons/user_icon.png", width=80)

    submit = False

    #Auswahl für Nutzer anlegen / anzeigen / suchen
    aktion = st.radio("Aktion auswählen", ["Nutzer anlegen", "Alle Nutzer anzeigen", "Nutzer suchen"])

    if aktion != "Alle Nutzer anzeigen":
        st.session_state["users_edit_user_id"] = None

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
                session_states.flash("Nutzer gespeichert")
                st.rerun()

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
                    st.session_state["users_edit_user_id"] = u.id

            with col4:
                delete_clicked = st.button("Löschen", key="delete_" + u.id)
                if delete_clicked:
                    u.delete()
                    #flash message wird angezeigt 
                    session_states.flash(f"Nutzer {u.id} gelöscht")
                    #Flash statt st.success direkt + rerun (sonst sieht man es nicht)
                    #wenn gerade derselbe Nutzer im Edit-Modus war: Edit-Modus beenden
                    if st.session_state["users_edit_user_id"] == u.id:
                        st.session_state["users_edit_user_id"] = None
                    st.rerun()

            #Edit-Block unter der Zeile NUR anzeigen, wenn dieser User ausgewählt ist
            if st.session_state["users_edit_user_id"] == u.id:
                st.info(f"Nutzer bearbeiten: {u.id}")

                # Form-Key muss eindeutig sein weil sonst vermischen von den form-states, deswegen + u.id
                with st.form("edit_form_" + u.id):
                    new_name = st.text_input("Neuer Name", value=u.name)
                    st.text_input("E-Mail-Adresse (ID)", value=u.id, disabled=True)
                    submit_row_edit = st.form_submit_button("Speichern")

                if submit_row_edit:
                    new_name = new_name.strip()
                    if new_name == "":
                        st.error("Name darf nicht leer sein")
                    else:
                        u.name = new_name
                        u.store_data()

                        #Flash message setzen, Edit-Modus schließen, dann rerunen
                        session_states.flash("Nutzer aktualisiert")
                        st.session_state["users_edit_user_id"] = None
                        st.rerun()

    # 3) Nutzer suchen 

    if aktion == "Nutzer suchen":

        users = User.find_all()

        if not users:
            st.info("Keine Nutzer vorhanden.")
            return

        with st.form("search_form"):
            search_email = st.text_input("Nutzer über E-Mail-Adresse suchen")
            search_name = st.text_input("Nutzer über Name suchen")
            search_clicked = st.form_submit_button("Suchen") 

        
        if search_clicked:
            if search_email.strip() != "":
                st.session_state["users_search_result"] = User.find_by_attribute("id", search_email.strip())
            elif search_name.strip() != "":
                st.session_state["users_search_result"] = User.find_by_attribute("name", search_name.strip())
            else:
                st.session_state["users_search_result"] = None

        search_result = st.session_state["users_search_result"]

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
                    session_states.flash("Nutzer aktualisiert")
                    st.session_state["users_search_result"] = None
                    st.rerun()

            delete_clicked = st.button("Nutzer löschen")
            if delete_clicked:
                search_result.delete()
                session_states.flash("Nutzer gelöscht")
                st.session_state["users_search_result"] = None
                st.rerun()

        elif search_clicked:
            st.warning("Kein Nutzer gefunden.")