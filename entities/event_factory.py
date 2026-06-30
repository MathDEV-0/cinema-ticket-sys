from entities.event import Event
from entities.event_child.movie_event import MovieEvent
from entities.event_child.music_show_event import MusicShowEvent
from entities.event_child.sports_game_event import SportsGameEvent


class EventFactory:

    @staticmethod
    def from_dict(data):
        event_type = data.get("event_type", "generic")
        if event_type == "movie":
            return MovieEvent(
                id=int(data["id"]),
                name=data["name"],
                duration=int(data["duration"]),
                genre=data.get("genre", ""),
                age_rating=int(data.get("age_rating", 0))
            )
        if event_type == "music":
            return MusicShowEvent(
                id=int(data["id"]),
                name=data["name"],
                duration=int(data["duration"]),
                artist=data.get("artist", ""),
                tour=data.get("tour", "")
            )
        if event_type == "sports":
            return SportsGameEvent(
                id=int(data["id"]),
                name=data["name"],
                duration=int(data["duration"]),
                home_team=data.get("home_team", ""),
                away_team=data.get("away_team", ""),
                championship=data.get("championship", "")
            )
        return Event(
            id=int(data["id"]),
            name=data["name"],
            duration=int(data["duration"]),
            event_type="generic"
        )