from datetime import date
import streamlit as st 
from devices import Device 
from maintenance import Maintenance
from session_states import flash


def ui_maintenance():      
    st.header("Wartungen")

    st.image("Icons/wartung_icon.png", width=80)

    devices = Device.find_all() or []

    if not devices: 
        st.info("Noch keine Geräte vorhanden. Bitte zuerst Geräte anlegen")
        return

    devices_by_id = {d.id: d for d in devices}
    labels = [f"{d.device_name} ({d.id})" for d in devices]
    label_to_id = {f"{d.device_name} ({d.id})": d.id for d in devices}


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

    st.divider()

    st.subheader("Nächste Wartungen")
    upcoming = Maintenance.upcoming()
    if not upcoming:
        st.info("Noch keine Wartungen eingetragen.")
    else:
        # Anzeige als einfache Tabelle
        rows = []
        for m in upcoming:
            rows.append({
                "Geräte-Name": m.device_name,
                "Geräte-ID": m.device_id,
                "Nächster Termin": m.next_maintenance_date,
                "€/Quartal": m.cost_per_quarter,
            })
        st.dataframe(rows, use_container_width=True)

    st.subheader("Wartungskosten pro Quartal")
    totals = Maintenance.costs_by_quarter()
    if not totals:
        st.info("Noch keine Kosten vorhanden.")
    else:
        #sortiert anzeigen
      for k in sorted(totals.keys()):
          st.write(f"{k}: {totals[k]:.2f} €")