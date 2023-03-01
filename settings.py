# -*- coding: utf-8 -*-
import os

from pygame.font import SysFont, Font
from pygame import init
from helper_func import loader

init()


XWIN, YWIN = 450, 700  # размер окна
HALF_XWIN, HALF_YWIN = XWIN / 2, YWIN / 2  # центр
DISPLAY = (XWIN, YWIN)
FLAGS = 0
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GREEN = (131, 252, 107)
ANDROID_GREEN = (164, 198, 57)
FOREST_GREEN = (87, 189, 68)

# игрок
PLAYER_SIZE = (25, 35)
PLAYER_IMG = loader.player
PLAYER_MAX_SPEED = 20
PLAYER_JUMPFORCE = 20
PLAYER_BONUS_JUMPFORCE = 70
GRAVITY = .9  # сложность

# платформы
PLATFORM_COLOR = loader.platform
PLATFORM_COLOR_LIGHT = loader.platform_break
PLATFORM_SIZE = (80, 10)
PLATFORM_DISTANCE_GAP = (50, 210)
MAX_PLATFORM_NUMBER = 10
BONUS_SPAWN_CHANCE = 10
BREAKABLE_PLATFORM_CHANCE = 12

# шрифты
LARGE_FONT = SysFont("", 128)
SMALL_FONT = SysFont("arial", 24)
fullname = os.path.join('data', 'fonts\\pixel_font.ttf')
pixel_font = Font(fullname, 20)
pixel_font_large = Font(fullname, 50)
