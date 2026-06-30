from entities.event import Event

class MovieEvent(Event):
    def __init__(self, id: int, name: str, duration: int, genre: str, age_rating: int):
        super().__init__(id, name, duration, event_type="movie")
        self.genre = genre
        self.age_rating = age_rating