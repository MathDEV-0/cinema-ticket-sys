from entities.event import Event

class MusicShow(Event):
    def __init__(self, name:str, duration:int, artist:str, tour:str):
        super().__init__(name, duration)
        self.artist = artist
        self.tour = tour