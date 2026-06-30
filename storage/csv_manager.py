import csv
import os

from entities.event import Event
from entities.room import Room
from entities.event_factory import EventFactory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "storage", "data")
TICKETS_PATH = os.path.join(DATA_DIR, "tickets.csv")
EVENTS_PATH = os.path.join(DATA_DIR, "events.csv")
ROOMS_PATH = os.path.join(DATA_DIR, "rooms.csv")

# Dentro da biblioteca CSV, há a função de converter dicionários em "tabelas", útil!
class CSVManager:
    @staticmethod
    def save(file_path, fieldnames, objects):
        with open(file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for obj in objects:
                writer.writerow(obj.to_dict())

    @staticmethod
    def load(file_path, factory=None):
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            if factory:
                return [factory(row) for row in rows]
            return rows
        
    @staticmethod
    def get_next_id(file_path):
        if not os.path.exists(file_path):
            return 1
        with open(file_path, "r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) <= 1:  # só header ou vazio
                return 1
            last_row = rows[-1]
            try:
                return int(last_row[0]) + 1
            except:
                return 1
   
    EVENT_CACHE = None

    @staticmethod
    def get_events():
        global EVENT_CACHE
        if EVENT_CACHE is None:
            EVENT_CACHE = CSVManager.load(EVENTS_PATH, EventFactory.from_dict)
        return EVENT_CACHE


    @staticmethod
    def find_event_by_id(event_id):
        return next(
            (e for e in CSVManager.get_events() if e.id == int(event_id)),
            None
        )

    @staticmethod
    def find_room_by_id(room_id):
        rooms = CSVManager.load(ROOMS_PATH, Room.from_dict)
        return next(
            (room for room in rooms if int(room.id) == int(room_id)),
            None
        )