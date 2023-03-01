from pygame import Rect
from pygame.sprite import Sprite

from singleton import Singleton
import settings as config


class Camera(Singleton):
    """
    A class to represent the camera.

    Manages level position scrolling.
    Can be access via Singleton: Camera.instance.
    (Check Singleton design pattern for more info)
  """

    def __init__(self, lerp=5, width=config.XWIN, height=config.YWIN):
        self.state = Rect(0, 0, width, height)
        self.lerp = lerp
        self.center = height // 2
        self.maxheight = self.center

    def reset(self):
        self.state.y = 0
        self.maxheight = self.center

    def apply_rect(self, rect):
        return rect.move((0, -self.state.topleft[1]))

    def apply(self, target):
        return self.apply_rect(target.rect)

    def update(self, target):
        # updating maxheight
        if target.y < self.maxheight:
            self.lastheight = self.maxheight
            self.maxheight = target.y

        # calculate scrolling speed required
        speed = (self.state.centery - self.maxheight) / self.lerp
        self.state.y -= speed