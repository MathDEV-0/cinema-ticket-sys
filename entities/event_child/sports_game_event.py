from entities.event import Event


class SportsGameEvent(Event):
    def __init__(self, id: int, name: str, duration: int, home_team: str, away_team: str, championship: str):
        super().__init__(id, name, duration, event_type="sports")
        self.home_team = home_team
        self.away_team = away_team
        self.championship = championship

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "event_type": self.event_type,
            "genre": "",
            "age_rating": "",
            "artist": "",
            "tour": "",
            "home_team": self.home_team,
            "away_team": self.away_team,
            "championship": self.championship
        }