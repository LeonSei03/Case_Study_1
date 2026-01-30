from datetime import date, datetime
from typing import Self
from serializer import Serializable
from database import DatabaseConnector
from devices import Device

class Maintenance(Serializable):

    db_connector =  DatabaseConnector().get_table("maintenance")

    def __init__(self, id, device_name: str,  device_id: str, next_maintenance_date: date, cost_per_quarter: float, creation_date: datetime = None, last_update: datetime = None) -> None:
        super().__init__(id, creation_date, last_update)
        self.device_name = device_name
        self.device_id = device_id
        self.next_maintenance_date = next_maintenance_date
        self.cost_per_quarter = float(cost_per_quarter)
    

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

