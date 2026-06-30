from datetime import datetime
from entities.event import Event
from entities.room import Room
from entities.seat import Seat
from storage.csv_manager import CSVManager

class Session:
    def __init__(self, id: int, event_id: int, room_id: int, start_time: datetime, price: float):
        self.id = id
        self.event_id = event_id
        self.room_id = room_id
        self.event = None
        self.room = None
        self.start_time = start_time
        self.price = price


    def can_sell(self):
        return datetime.now() < self.start_time


    def reserve_seat(self, seat: Seat):
        if not self.can_sell():
            raise ValueError(
                "Sessão já iniciada"
            )

        seat.reserve()
    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "room_id": self.room_id,
            "start_time": self.start_time.isoformat(),
            "price": self.price
        }

    @staticmethod
    def from_dict(data):
        return Session(
            id=int(data["id"]),
            event_id=int(data["event_id"]),
            room_id=int(data["room_id"]),
            start_time=datetime.fromisoformat(data["start_time"]),
            price=float(data["price"])
        )
    
    @staticmethod
    def load_with_relations(data, events, rooms):
        """Carrega uma sessão com suas relações"""
        session = Session.from_dict(data)
        # Carrega o evento relacionado
        session.event = next((e for e in events if e.id == session.event_id), None)
        # Carrega a sala relacionada
        session.room = next((r for r in rooms if r.id == session.room_id), None)
        return session