from enum import Enum

class Direction(Enum):
    NONE = "None"
    ALL = "All Directions"
    NORTH = "Northbound"
    EAST = "Eastbound"
    SOUTH = "Southbound"
    WEST = "Westbound"
    INBOUND = "Inbound"
    OUTBOUND = "Outbound"
    BOTH = "Both Directions"
    UNKNOWN = "Unknown"