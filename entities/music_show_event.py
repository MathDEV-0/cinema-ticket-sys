from entities.event import Event

class MusicShow(Event):
    def __init__(self, name, duration, artist, tour):
        super().__init__(name, duration)
        self.artist = artist
        self.tour = tour