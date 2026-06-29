from entities.event import Event

class MovieEvent(Event):
    def __init__(self, name: str, duration:int, genre: str, age_rating: int):
        super().__init__(name, duration)
        self.genre = genre
        self.age_rating = age_rating
