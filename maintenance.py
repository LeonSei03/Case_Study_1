from datetime import date, datetime
from typing import Self
from serializer import Serializable
from database import DatabaseConnector
from devices import Device

class Maintenance(Serializable):

    db_connector =  DatabaseConnector().get_table("maintenance")

    def __init__(self, id, device_name: str,  device_id: str, next_maintenance_date: date, cost_per_quarter: float, creation_date: datetime = None, last_update: datetime = None) -> None:
        super().__init__(id, creation_date, last_update)
        #self.id = id
        self.device_name = device_name
        self.device_id = device_id
        self.next_maintenance_date = next_maintenance_date
        self.cost_per_quarter = int(cost_per_quarter)
    

    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data["id"], data['device_name'], data["device_id"], data["next_maintenance_date"], data["cost_per_quarter"], data['creation_date'], data['last_update'])

    def __str__(self):
        return f"Maintenance: {self.device_id} {self.next_maintenance_date} ({self.cost_per_quarter} Euro pro Quartal)"

    @classmethod
    def upcoming(cls) -> list[Self]:
        items = cls.find_all()
        items.sort(key=lambda m: m.next_maintenance_date)
        return items
    
    @staticmethod
    def quarter_key(d: date) -> str:
        q = ((d.month - 1) // 3) + 1
        return f"{d.year}-Q{q}"

    @classmethod
    def costs_by_quarter(cls) -> dict[str, float]:
        totals: dict[str, float] = {}
        for m in cls.find_all():
            key = cls.quarter_key(m.next_maintenance_date)
            totals[key] = totals.get(key, 0.0) + float(m.cost_per_quarter)
        return totals

if __name__ == "__main__":
    #Device anlegen
    d = Device("Laser Cutter", "DEV-001", "one@mci.edu")
    d.store_data()

    #Maintenance für dieses Device anlegen
    m = Maintenance(
        device_name="Gerät",
        device_id="DEV-001",
        id="MNT-DEV-001-2026-02-01",
        next_maintenance_date=date(2026, 2, 1),
        cost_per_quarter=120
    )
    m.store_data()

    #Test: wieder laden
    loaded = Maintenance.find_by_attribute("device_id", "DEV-001")
    print("Loaded:", loaded)

    # alle Wartungen
    for x in Maintenance.find_all():
        print(x)
