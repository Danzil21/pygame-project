import pygame
import os
import sys


def load_image(name, colorkey=None):
    """Загрузка изображений"""

    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()

    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 1))
        image.set_colorkey(colorkey)
    else:
        pass

    return image