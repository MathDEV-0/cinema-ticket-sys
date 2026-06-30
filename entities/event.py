class Event:
    def __init__(self, id: int, name: str, duration: int, event_type: str = "generic"):
        self.id = id
        self.name = name
        self.duration = duration
        self.event_type = event_type

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "event_type": self.event_type
        }