import math
import pygame
from pygame.locals import KEYDOWN, KEYUP, K_LEFT, K_RIGHT
from sprites.sprite import PlayerSprite
from models.level import Level
import settings as config
from helper_func import loader


class Player(PlayerSprite):
    """Класс, отвечающий за физику и передвижение дудла"""
    def __init__(self, *args):
        super().__init__(*args)
        self.__image = pygame.transform.scale(loader.player, (50, 50))
        self.__startrect = self.__image.copy()
        self.__maxvelocity = pygame.math.Vector2(config.PLAYER_MAX_SPEED, 100)
        self.__startspeed = 1.5

        self._velocity = pygame.math.Vector2()
        self._input = 0
        self._jumpforce = config.PLAYER_JUMPFORCE
        self._bonus_jumpforce = config.PLAYER_BONUS_JUMPFORCE

        self.gravity = config.GRAVITY
        self.accel = 0.5
        self.deccel = 0.6
        self.dead = False

    def _fix_velocity(self):
        self._velocity.y = min(self._velocity.y, self.__maxvelocity.y)
        self._velocity.y = round(max(self._velocity.y, -self.__maxvelocity.y), 2)
        self._velocity.x = min(self._velocity.x, self.__maxvelocity.x)
        self._velocity.x = round(max(self._velocity.x, -self.__maxvelocity.x), 2)

    def reset(self):
        self._velocity = pygame.math.Vector2()
        self.rect = self.__startrect.copy().get_rect()
        self.camera_rect = self.__startrect.copy().get_rect()
        self.dead = False

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self._velocity.x = -self.__startspeed
                self._input = -1
            elif event.key == K_RIGHT:
                self._velocity.x = self.__startspeed
                self._input = 1
        elif event.type == KEYUP:
            if (event.key == K_LEFT and self._input == -1) or (event.key == K_RIGHT and self._input == 1):
                self._input = 0

    def jump(self, force=None):
        if force is None:
            force = self._jumpforce
        self._velocity.y = -force

    def on_collide(self, obj):
        self.rect.bottom = obj.rect.top
        self.jump()

    def collisions(self):
        lvl = Level.instance
        if lvl is None:
            return
        for platform in lvl.platforms:
            if self._velocity.y > 0.5:
                if platform.bonus and pygame.sprite.collide_rect(self, platform.bonus):
                    self.on_collide(platform.bonus)
                    self.jump(platform.bonus.force)
                if pygame.sprite.collide_rect(self, platform):
                    self.on_collide(platform)
                    platform.on_collide()

    def update(self):
        if self.camera_rect.y > config.YWIN * 2:
            self.dead = True
            return
        self._velocity.y += self.gravity
        if self._input:
            self._velocity.x += self._input * self.accel
        elif self._velocity.x:
            self._velocity.x -= math.copysign(self.deccel, self._velocity.x)
            self._velocity.x = round(self._velocity.x)
        self._fix_velocity()
        self.rect.x = (self.rect.x + self._velocity.x) % (config.XWIN - self.rect.width)
        self.rect.y += self._velocity.y
        self.collisions()
