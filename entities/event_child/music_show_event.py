from entities.event import Event

class MusicShowEvent(Event):
    def __init__(self, id: int, name: str, duration: int, artist: str, tour: str):
        super().__init__(id, name, duration, event_type="music")
        self.artist = artist
        self.tour = tour