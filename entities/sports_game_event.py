from entities.event import Event


class SportsGameEvent(Event):
    def __init__(self, name, duration, home_team, away_team, championship):
        super().__init__(name, duration)
        self.home_team = home_team
        self.away_team = away_team
        self.championship = championship