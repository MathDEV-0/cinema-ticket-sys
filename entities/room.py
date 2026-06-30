import os
from entities.seat import Seat


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Room:

    def __init__(self, id: int, name:str,  file_path: str):
        self.id = id
        self.name = name
        self.file_path = file_path
        self.layout = self.load_layout(file_path)

    def load_layout(self, file_path: str):
        full_path = os.path.join(BASE_DIR, "storage", "rooms", file_path)
        matrix = []
        with open(full_path, "r") as file:
            for row_index, line in enumerate(file):
                row = []
                for col_index, value in enumerate(line.split()):
                    value = int(value)

                    if value == 0:
                        row.append(Seat(row_index, col_index))
                    elif value == 4:
                        row.append(Seat(row_index, col_index, accessible=True))
                    else:
                        row.append(None)

                matrix.append(row)

        return matrix
    
    def get_seat(self, label):
        label = label.upper().strip()
        if len(label) < 2:
            raise ValueError("Assento inválido.")
        try:
            row = ord(label[0]) - ord("A")
            column = int(label[1:]) - 1
        except ValueError:
            raise ValueError("Formato inválido. Exemplo: A10")
        if row < 0 or row >= len(self.layout):
            raise ValueError("Linha inexistente.")
        if column < 0 or column >= len(self.layout[row]):
            raise ValueError("Coluna inexistente.")
        seat = self.layout[row][column]
        if not isinstance(seat, Seat):
            raise ValueError("Não existe assento nessa posição.")
        return seat

    def __str__(self):
        max_cols = max(len(row) for row in self.layout)
        text = "\n   "
        for col in range(max_cols):
            text += f"{col+1:>3}"
        text += "\n"
        #Itera pelo layout da matriz
        for row_index, row in enumerate(self.layout):
            text += f"{chr(ord('A')+row_index):>2}  "
            for item in row:
                # Verifica se é um objeto Seat
                if isinstance(item, Seat):
                    text += f"{item.icon} "
                # Se não, é corredor                    
                else:
                    text += "   "
            text += "\n"
        text += "======================= TELA =======================\n🟩 Disponível   🟥 Ocupado   ♿ Acessível"

        return text
    
    @staticmethod
    def from_dict(data):
        return Room(
            id=int(data["id"]),
            name=data["name"],
            file_path=data["file_path"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "file_path": self.file_path
        }