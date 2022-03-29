from enum import Enum

class MapsMooveException(Enum):
    ARROW_DAYS = (82, 174, 222)
    VALIDATE_RESA = (81, 174, 222)
    RED_WAIT = (216, 68, 79)

class PixelMoove(Enum):
    UP_START = (377, 33)
    DOWN_START = (1456, 905)
    RIGHT_START = (1575, 74)
    LEFT_START = (334, 838)
    UP_END = (1495, 33)
    DOWN_END = (504, 905)
    RIGHT_END = (1575, 855)
    LEFT_END = (334, 46)
    UP_MIDDLE = (559, 33)
    DOWN_MIDDLE = (476, 905)
    RIGHT_MIDDLE = (1575, 391)
    LEFT_MIDDLE = (334, 396)

class MapsGraph(Enum):
    adjac_lis_dof = {
    (5,10): {(5,11) : PixelMoove.UP_MIDDLE, (6,10) : PixelMoove.RIGHT_MIDDLE, (5,9) : PixelMoove.DOWN_MIDDLE, (4,10) : PixelMoove.LEFT_MIDDLE},
    (5,11): {(5,10) : PixelMoove.DOWN_MIDDLE},
    (6,10): {(5,10) : PixelMoove.LEFT_MIDDLE},
    (4,10): {(5,10) : PixelMoove.RIGHT_MIDDLE},
    (5,9): {(5,10) : PixelMoove.UP_MIDDLE}
    }