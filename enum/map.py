from enum import Enum

class MapsMooveException(Enum):
    ARROW_DAYS = (82, 174, 222)
    VALIDATE_RESA = (81, 174, 222)
    RED_WAIT = (216, 68, 79)

class PixelMoove(Enum):
    UP = (500,500)
    DOWN = (500,500)
    RIGHT = (500,500)
    LEFT = (500,500)

class MapsGraph(Enum):
    adjac_lis = {
    'A': ['B','C','D'],
    'B': ['D'],
    'C': ['D']
    }