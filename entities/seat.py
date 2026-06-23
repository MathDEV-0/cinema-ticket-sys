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