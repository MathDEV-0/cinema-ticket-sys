from entities.event import Event

class MovieEvent(Event):
    def __init__(self, id: int, name: str, duration: int, genre: str, age_rating: int):
        super().__init__(id, name, duration, event_type="movie")
        self.genre = genre
        self.age_rating = age_rating

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "event_type": self.event_type,
            "genre": self.genre,
            "age_rating": self.age_rating,
            "artist": "",
            "tour": "",
            "home_team": "",
            "away_team": "",
            "championship": ""
        }