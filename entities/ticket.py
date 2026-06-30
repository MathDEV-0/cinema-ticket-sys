from entities.user import User
from entities.session import Session
from entities.seat import Seat

class Ticket:
    def __init__(self, id: int, user: User = None, session: Session = None, seat: Seat = None,
                 price: float = 0.0, status: str = "ativo", user_id: int = None, session_id: int = None):
        self.id = id
        self.user = user
        self.session = session
        self.seat = seat
        self.price = price
        self.status = status
        # Guarda os IDs para referência
        self.user_id = user_id if user_id is not None else (user.id if user else None)
        self.session_id = session_id if session_id is not None else (session.id if session else None)

    def cancel(self):
        if self.status == "usado":
            raise ValueError("Ingresso já utilizado")
        self.status = "cancelado"
        if self.seat:
            self.seat.release()

    def use(self):
        if self.status != "ativo":
            raise ValueError("Ingresso inválido")
        self.status = "usado"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user.id if self.user else self.user_id,
            "session_id": self.session.id if self.session else self.session_id,
            "seat_row": self.seat.row if self.seat else None,
            "seat_col": self.seat.column if self.seat else None,
            "price": self.price,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Ticket(
            id=int(data["id"]),
            user=None,
            session=None,
            seat=Seat(int(data["seat_row"]), int(data["seat_col"])),
            price=float(data["price"]),
            status=data["status"],
            user_id=int(data["user_id"]),
            session_id=int(data["session_id"])
        )