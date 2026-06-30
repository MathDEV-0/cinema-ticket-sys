class Seat:

    def __init__(self, row: int, column: int, accessible: bool = False):
        self.row = row
        self.column = column
        self.accessible = accessible
        self.status = "disponível"

    def reserve(self):
        if self.status != "disponível":
            raise ValueError("Assento indisponível")

        self.status = "reservado"

    def release(self):
        self.status = "disponível"

    def sell(self):
        if self.status != "reservado":
            raise ValueError("Assento deve estar reservado antes da venda")

        self.status = "vendido"

    @property
    def icon(self):
        if self.accessible:
            return "♿"

        if self.status == "disponível":
            return "🟩"

        return "🟥"

    @property
    def label(self):
        row = chr(ord("A") + self.row)
        return f"{row}{self.column + 1}"
    
    # Utils para CSV
    def to_dict(self):
        return {
            "row": self.row,
            "column": self.column,
            "accessible": self.accessible,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        seat = Seat(
            int(data["row"]),
            int(data["column"]),
            data["accessible"] == "True"
        )
        seat.status = data.get("status", "disponível") 
        return seat