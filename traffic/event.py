from .direction import Direction

from datetime import datetime
from enum import Enum

class EventType(Enum):
    ACCIDENT = "accidentsAndIncidents"
    ROADWORK = "roadwork"
    EVENT = "specialEvents"
    CLOSURE = "closures"
    TRANSIT = "transitMode"
    INFO = "generalInfo"
    WINTER = "winterDrivingIndex"

class Schedule:
    def __init__(
        self,
        id: str,
        start: str,
        end: str,
        continuous: str,
        active_days: [str],
    ):
        self.id = int(id)
        self.start = start
        self.end = end
        self.continuous = continuous == "true"
        self.active_days = active_days

def parse_datetime(datetime: str) -> datetime:
    return datetime.strptime(datetime, "%d/%m/%YT%H:%M:%S")

class Event:
    def __init__(
        self,
        id: int,
        region: str,
        county: str,
        severity: str,
        roadway: str,
        direction: str,
        description: str,
        location: str,
        lanes_affected: str,
        lanes_status: str,
        navteq_id: str,
        start_location: str,
        end_location: str,
        start_city: str,
        end_city: str,
        event_type: str,
        event_subtype: str,
        polyline: str,
        last_updated: str,
        latitude: str,
        longitude: str,
        start_date: str,
        end_date: str,
        reported: str,
        schedule: Schedule,
    ):
        self.id = int(id)
        self.region = region
        self.county = county
        self.severity = severity
        self.roadway = roadway
        self.direction = Direction(direction)
        self.description = description
        self.location = location
        self.lanes_affected = lanes_affected
        self.lanes_status = lanes_status
        self.navteq_id = navteq_id
        self.start_location = start_location
        self.end_location = end_location
        self.start_city = start_city
        self.end_city = end_city
        self.event_type = EventType(event_type)
        self.event_subtype = event_subtype
        self.polyline = polyline
        self.last_updated = parse_datetime(last_updated)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.start_date = parse_datetime(start_date)
        self.end_date = parse_datetime(end_date)
        self.reported = parse_datetime(reported)
        self.schedule = schedule