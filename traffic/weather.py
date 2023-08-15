class RoadCondition:
    def __init__(
        self,
        condition: str,
        area: str,
        location: str,
        roadway: str,
        polyline: str,
        last_updated: str,
    ):
        self.condition = condition
        self.area = area
        self.location = location
        self.roadway = roadway
        self.polyline = polyline
        self.last_updated = int(last_updated)