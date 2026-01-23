from datetime import date
import streamlit as st 
from devices import Device 
from maintenance import Maintenance
import session_states
from session_states import flash
from session_states import session_states


def ui_maintenance():      
    st.header("Wartungen")

    st.image("Icons/wartung_icon.png", width=80)

    devices = Device.find_all() or []

    aktion = st.radio("Aktion auswählen", ["Wartung anlegen", "Alle Wartungen anzeigen"])

    if aktion != "Alle Wartungen anzeigen":
        st.session_state["edit_maintenance"] = None

    if not devices: 
        st.info("Noch keine Geräte vorhanden. Bitte zuerst Geräte anlegen")
        return

    devices_by_id = {d.id: d for d in devices}
    labels = [f"{d.device_name} ({d.id})" for d in devices]
    label_to_id = {f"{d.device_name} ({d.id})": d.id for d in devices}

    if aktion == "Wartung anlegen":

        st.subheader("Wartung anlegen oder aktualisieren")


        with st.form("maintenance-form"):
            selected_label = st.selectbox("Gerät wählen", options=labels)
            device_id = label_to_id[selected_label]

            device = devices_by_id[device_id]
            device_name = device.device_name

            next_date = st.date_input("Nächster Wartungstermin", value=date.today())
            cost = st.number_input("Wartungskosten pro Quartal (€)", min_value=0.0, step=10.0)

            submit = st.form_submit_button("Speichern")

        if submit:
            # einfache ID-Strategie: pro Gerät + Datum eindeutig
            m_id = f"MNT-{device_id}-{next_date.isoformat()}"
            m = Maintenance(
                id=m_id,
                device_name=device_name,
                device_id=device_id,
                next_maintenance_date=next_date,
                cost_per_quarter=cost,
            )
            m.store_data()
            flash("Wartung gespeichert")  # oder st.success(...)
            st.rerun()

    if aktion == "Alle Wartungen anzeigen":

        st.subheader("Nächste Wartungen")

        upcoming = Maintenance.upcoming()

        if not upcoming:
            st.info("Noch keine Wartungen eingetragen.")
            return
         
        st.subheader("Nächste Wartungen")
            # Anzeige als einfache Tabelle
        for m in upcoming: 
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])

            with col1:
                st.write(m.device_name)

            with col2: 
                st.write(m.device_id)
            
            with col3: 
                st.write(m.next_maintenance_date)

            with col4:
                st.write(m.cost_per_quarter)

            with col5:
                edit_clicked = st.button("Ändern", key="edit_" + m.id)
                if edit_clicked:
                    st.session_state["edit_maintenance"] = m.id

            with col6:
                delete_clicked = st.button("Löschen", key="delete_" + m.id)
                if delete_clicked:
                    m.delete()
                    #flash message wird angezeigt 
                    flash(f"Wartung {m.id} gelöscht")
                    #Flash statt st.success direkt + rerun (sonst sieht man es nicht)
                    #wenn gerade derselbe Nutzer im Edit-Modus war: Edit-Modus beenden
                    if st.session_state["users_edit_user_id"] == m.id:
                        st.session_state["users_edit_user_id"] = None
                    st.rerun()

        st.subheader("Wartungskosten pro Quartal")
        totals = Maintenance.costs_by_quarter()
        if not totals:
            st.info("Noch keine Kosten vorhanden.")
        else:
                #sortiert anzeigen
            for k in sorted(totals.keys()):
                st.write(f"{k}: {totals[k]:.2f} €")
    
    