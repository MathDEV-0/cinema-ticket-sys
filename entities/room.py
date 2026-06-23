from entities.seat import Seat


class Room:

    def __init__(self, file_path: str):
        self.layout = self.load_layout(file_path)

    def load_layout(self, file_path: str):
        matrix = []
        with open(file_path, "r") as file:
            for row_index, line in enumerate(file):
                row = []
                for col_index, value in enumerate(line.split()):
                    value = int(value)
                    if value == 0:
                        row.append(Seat(row_index, col_index))
                    elif value == 4:
                        row.append(Seat(row_index,col_index,accessible=True))
                    else:
                        row.append(value)
                matrix.append(row)
        return matrix