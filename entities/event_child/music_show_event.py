from entities.event import Event

class MusicShowEvent(Event):
    def __init__(self, id: int, name: str, duration: int, artist: str, tour: str):
        super().__init__(id, name, duration, event_type="music")
        self.artist = artist
        self.tour = tour

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "event_type": self.event_type,
            "genre": "",
            "age_rating": "",
            "artist": self.artist,
            "tour": self.tour,
            "home_team": "",
            "away_team": "",
            "championship": ""
        }