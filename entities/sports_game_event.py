from entities.event import Event


class SportsGameEvent(Event):
    def __init__(self, name:str, duration:int, home_team:str, away_team:str, championship:str):
        super().__init__(name, duration)
        self.home_team = home_team
        self.away_team = away_team
        self.championship = championship