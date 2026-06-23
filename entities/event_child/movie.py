from entities import Event

class Movie(Event):
    def __init__(self, name, duration, director):
        super().__init__(name, duration)
        self.director = director