from datetime import date
import streamlit as st 
from devices import Device 
from maintenance import Maintenance
from session_states import flash

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
            # einfache ID: pro Gerät + Datum eindeutig
            m_id = f"MNT-{device_id}-{next_date.isoformat()}"
            m = Maintenance(
                id=m_id,
                device_name=device_name,
                device_id=device_id,
                next_maintenance_date=next_date,
                cost_per_quarter=cost,
            )
            m.store_data()
            flash("Wartung gespeichert")  # oder st.success
            st.rerun()

    if aktion == "Alle Wartungen anzeigen":

        st.subheader("Nächste Wartungen")

        upcoming = Maintenance.upcoming()

        if not upcoming:
            st.info("Noch keine Wartungen eingetragen.")
            return
         
        st.subheader("Nächste Wartungen")

        h1, h2, h3, h4, h5, h6 = st.columns([2, 2, 2, 2, 2, 2])

        with h1: st.markdown("Gerätename")

        with h2: st.markdown("Geräte ID")

        with h3: st.markdown("Wartung am")

        with h4: st.markdown("Kosten")

        with h5: st.markdown("Ändern")

        with h6: st.markdown("Löschen")


        #Anzeige als einfache Tabelle
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
                    flash(f"Wartung für {m.device_name} gelöscht")
                    if st.session_state["edit_maintenance"] == m.id:
                        st.session_state["edit_maintenance"] = None
                    st.rerun()

            if st.session_state["edit_maintenance"] == m.id:
                st.info(f"Wartung bearbeiten: {m.device_name}")

                #Form-Key muss eindeutig sein weil sonst vermischen von den form-states deswegen + u.id
                with st.form("edit_form_" + m.id):
                    new_cost = st.number_input("Neue Kosten",min_value=0.0, step=10.0, value=float(m.cost_per_quarter), key=f"edit_cost_{m.id}")
                    new_date = st.date_input("Neues Datum", value=m.next_maintenance_date, key=f"edit_date_{m.id}")
                    submit_row_edit = st.form_submit_button("Speichern")

                if submit_row_edit:
                    m.cost_per_quarter = float(new_cost)
                    m.next_maintenance_date = new_date
                    m.store_data()

                    #Flash message setzen, Edit-Modus schließen, dann rerunen
                    flash("Wartung aktualisiert")
                    st.session_state["edit_maintenance"] = None
                    st.rerun()

        st.subheader("Wartungskosten pro Quartal")
        totals = Maintenance.costs_by_quarter()
        if not totals:
            st.info("Noch keine Kosten vorhanden.")
        else:
                #sortiert anzeigen
            for k in sorted(totals.keys()):
                st.write(f"{k}: {totals[k]:.2f} €")
    
    