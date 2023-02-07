from enum import Enum

SCREEN_SIZE = (900, 1000)


class Color(Enum):
    RED = (255, 0, 0)
    LIGHT_RED = (255, 102, 102)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (102, 178, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    CYAN = (0, 255, 255)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)
    GREY = (128, 128, 128)


class Scene(Enum):
    MAIN_MENU = 0
    TURNS = 1
    HUMAN_VS_IA = 2
    AI_VS_AI = 3