import streamlit as st
from devices import Device
from users import User
import ui_devices
import ui_users
import session_states
from typing import Self
from datetime import date
from serializer import Serializable
from database import DatabaseConnector
from uuid import uuid4
from reservations import Reservations


# Vorbedingung: Gerät ist angelegt und passender Nutzer ist angelegt
# Nachbedingung: Reservierung ist angelegt oder entfernt

def ui_reservations():

    st.header("Reservierungen")
    st.image("Icons/kalender_icon.png", width=80)

    session_states.flash_anzeigen()

    devices = Device.find_all() or []
    users = User.find_all() or []

    if not devices:
        st.info("Kein Gerät vorhanden. Bitte erst ein Gerät anlegen!")
        return
    
    if not users:
        st.info("Kein Nutzer vorhanden. Bitte erst einen Nutzer anlegen")
        return

    # Geräte auswählen zum Reservieren
    selected_device = st.selectbox(
                            "Gerät wählen",    
                            devices,
                            format_func=lambda d: f"{d.id} - {d.device_name}")

    selected_user = st.selectbox(
                        "Nutzer wählen",
                        users,
                        format_func=lambda u: f"{u.name} - {u.id}")

    with st.form("reserve_form"):
        start_date = st.date_input("Startdatum", value=date.today())
        end_date = st.date_input("Enddatum", value=date.today())
        purpose = st.text_input("Projekt / Zweck")
        submit = st.form_submit_button("Reservierung eintragen")

    # Button klick
    if submit:
        purpose = (purpose or "").strip() # mit strip() leerzeichen entfernen

        # schauen ob ein Zweck eingegeben wurde
        if purpose == "":
            session_states.flash("Bitte Projekt/Zweck angeben.", "error")
            st.rerun()

        # gucken das erste datum eingabe passt
        if start_date > end_date:
            session_states.flash("Startdatum darf nicht nach dem Enddatum liegen.", "error")
            st.rerun()

        # auf konflikte, also überlappung der Daten prüfen
        conflicts = Reservations.find_conflicts(
            device_id=selected_device.id,
            start_date=start_date,
            end_date=end_date,
        )

        if conflicts:
            # Konflikte anzeigen
            session_states.flash("Konflikt: Zeitraum überschneidet sich mit bestehender Reservierung.", "error")
            st.write("Reservierung überschneidet sich:")
            for c in conflicts:
                st.write(f"- {c.start_date} bis {c.end_date} | {c.user_id} | {c.purpose}")
            return

        # Speichern
        new_res = Reservations(
            id=str(uuid4()),
            device_id=selected_device.id,
            user_id=selected_user.id,
            start_date=start_date,
            end_date=end_date,
            purpose=purpose,
        )
        new_res.store_data()

        session_states.flash("Reservierung gespeichert.", "success")
        st.rerun()

    # Bestehende Reservierungen anzeigen + löschen
    st.subheader("Bestehende Reservierungen für dieses Gerät")
    res_list = Reservations.find_by_device(selected_device.id)

    if not res_list:
        st.info("Noch keine Reservierungen.")
    else:
        # kleine Tabelle mit Spalten
        h1, h2, h3, h4, h5 = st.columns([2, 2, 3, 4, 2])
        h1.write("**Start**")
        h2.write("**Ende**")
        h3.write("**User**")
        h4.write("**Zweck**")
        h5.write("**Aktion**")

        for r in res_list:
            c1, c2, c3, c4, c5 = st.columns([2, 2, 3, 4, 2])
            c1.write(str(r.start_date))
            c2.write(str(r.end_date))
            c3.write(r.user_id)
            c4.write(r.purpose)

            # eindeutiger Key, damit Streamlit Buttons auseinanderhalten kann
            if c5.button("Löschen", key=f"delete_res_{r.id}"):
                r.delete()
                session_states.flash("Reservierung gelöscht.", "success")
                st.rerun()
