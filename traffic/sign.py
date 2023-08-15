from .direction import Direction

class Sign:
    def __init__(
        self,
        id: str,
        name: str,
        roadway: str,
        direction: str,
        messages: [str],
        latitude: str,
        longitude: str,
    ):
        self.id = id
        self.name = name
        self.roadway = roadway
        self.direction = Direction(direction)
        self.messages = messages
        self.latitude = float(latitude)
        self.longitude = float(longitude)