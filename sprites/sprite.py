from pygame import Surface, Rect
from models.camera import Camera
import pygame

class Sprite:
    def __init__(self, x: int, y: int, w: int, h: int, color, img=True, bonus=False):
        self.__color = color
        if not img:
            self._image = Surface((w, h))
            self._image.fill(self.__color)
            self._image = self._image.convert()
            self.rect = Rect(x, y, w, h)
        else:
            self._image = pygame.transform.scale(color, (100, 20) if not bonus else (50, 20))
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
        self.camera_rect = self.rect.copy()

    @property
    def image(self) -> Surface:
        return self._image

    @property
    def color(self) -> tuple:
        return self.__color

    @color.setter
    def color(self, new: tuple) -> None:
        self.__color = new
        self._image.fill(self.color)

    def draw(self, surface: Surface) -> None:
        if Camera.instance:
            self.camera_rect = Camera.instance.apply(self)
            surface.blit(self._image, self.camera_rect)
        else:
            surface.blit(self._image, self.rect)


class PlayerSprite:
    def __init__(self, img, size):
        self.__color = img
        self._image = pygame.transform.scale(img, size)
        self.rect = self.image.get_rect()
        self.camera_rect = self.rect.copy()

    @property
    def image(self) -> Surface:
        return self._image

    @property
    def color(self) -> tuple:
        return self.__color

    @color.setter
    def color(self, new: tuple) -> None:
        self.__color = new
        # update image surface
        self._image.fill(self.color)

    def draw(self, surface: Surface) -> None:
        if Camera.instance:
            self.camera_rect = Camera.instance.apply(self)
            surface.blit(self._image, self.camera_rect)
        else:
            surface.blit(self._image, self.rect)
