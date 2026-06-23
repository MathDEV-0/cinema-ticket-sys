from entities.user import User
from entities.session import Session
from entities.seat import Seat

class Ticket:
    def __init__(self, user: User, session: Session, seat: Seat, price: float):
        self.user = user
        self.session = session
        self.seat = seat
        self.price = price
        self.status = "ativo"

    def cancel(self):
        if self.status == "usado":
            raise ValueError("Ingresso já utilizado")

        self.status = "cancelado"
        self.seat.release()

    def use(self):
        if self.status != "ativo":
            raise ValueError("Ingresso inválido")

        self.status = "usado"