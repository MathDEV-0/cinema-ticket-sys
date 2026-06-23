from datetime import datetime
from entities.event import Event
from entities.room import Room
from entities.seat import Seat

class Session:
    def __init__(self, event: Event, room: Room, start_time: datetime, price: float):
        self.event = event
        self.room = room
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