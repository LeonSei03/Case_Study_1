from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Self, List, Optional
from uuid import uuid4

from tinydb import Query

from serializer import Serializable
from database import DatabaseConnector

# Vorbedingung: Gerät ist angelegt und passender Nutzer ist angelegt
# Nachbedingung: Reservierung ist angelegt oder entfernt

class Reservations(Serializable):

    db_connector = DatabaseConnector().get_table("reservations")

    def __init__(
        self,
        id: str,
        device_id: str,
        user_id: str,
        start_date: date,
        end_date: date,
        purpose: str,
        creation_date: datetime = None,
        last_update: datetime = None,):
            
        super().__init__(id, creation_date, last_update)
        self.device_id = device_id
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.purpose = purpose

    # wandelt unseren Datensatz (Dict) von der TinyDB in ein Reservation-Objekt um
    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(            
            data["id"],
            data["device_id"],
            data["user_id"],
            data["start_date"],
            data["end_date"],
            data.get("purpose", ""),
            data.get("creation_date"),
            data.get("last_update"),)

    def __str__(self) -> str:
        return (
            f"Reservation {self.id}: device={self.device_id}, user={self.user_id}, "
            f"{self.start_date}..{self.end_date} ({self.purpose})")

    # Prüfen ob sich Datumsbereiche überschneiden
    # True -> es gibt eine Überschneidung
    # False -> keine Überschneidung
    @staticmethod #staticmethod weil kein self
    def _ueberlappung(
        a_start: date,
        a_end: date,
        b_start: date,
        b_end: date) -> bool:

        # gibt uns eine Überschneidung zurück
        return not (a_end < b_start or b_end < a_start)

    # gibt uns alle Reservierungen für bestimmtes Gerät
    @classmethod
    def find_by_device(cls, device_id: str) -> List["Reservations"]:
        q = Query()
        rows = cls.db_connector.search(q.device_id == device_id)  # <- WICHTIG
        res = [cls.instantiate_from_dict(r) for r in rows] if rows else []
        res.sort(key=lambda r: (r.start_date, r.end_date))
        return res

    # prüft ob es konflikte bei bestehenden Reservierungen gibt -> Gibt Liste an Konflikten zurück
    @classmethod
    def find_conflicts(
        cls,
        device_id: str,
        start_date: date,
        end_date: date,
        ignore_reservation_id: Optional[str] = None,
    ) -> List["Reservations"]:
        conflicts: List["Reservations"] = []
        for r in cls.find_by_device(device_id):
            if ignore_reservation_id and r.id == ignore_reservation_id:
                continue
            if cls._ueberlappung(start_date, end_date, r.start_date, r.end_date):
                conflicts.append(r)
        return conflicts