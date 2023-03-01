from random import randint
from pygame import Surface
import asyncio

from singleton import Singleton
from sprites.sprite import Sprite
import settings as config
from helper_func import loader


def chance(x):
    return not randint(0, x)


class Bonus(Sprite):
    WIDTH = 15
    HEIGHT = 15

    def __init__(self, parent: Sprite, color=loader.platform_trampoline,
                 force=config.PLAYER_BONUS_JUMPFORCE):
        self.parent = parent
        self.bonus = True
        super().__init__(*self._get_initial_pos(),
                         Bonus.WIDTH, Bonus.HEIGHT, color, True, True)
        self.force = force

    def _get_initial_pos(self):
        x = self.parent.rect.centerx - Bonus.WIDTH
        y = self.parent.rect.y - Bonus.HEIGHT
        return x, y


class Platform(Sprite):
    """Одноимённый класс отвечает за платформы в игре"""
    def __init__(self, x: int, y: int, width: int, height: int,
                 initial_bonus=False, breakable=False):

        color = config.PLATFORM_COLOR
        if breakable:
            color = config.PLATFORM_COLOR_LIGHT

        super().__init__(x, y, width, height, color)

        self.breakable = breakable
        self.__level = Level.instance
        self.__bonus = None
        if initial_bonus:
            self.add_bonus(Bonus)

    @property
    def bonus(self):
        return self.__bonus

    def add_bonus(self, bonus_type: type) -> None:
        """Добавляет батут на платформу"""
        if not self.__bonus and not self.breakable:
            self.__bonus = bonus_type(self)

    def remove_bonus(self) -> None:
        """Убирает батут с платформы."""
        self.__bonus = None

    def on_collide(self) -> None:
        """Убирает сломаную платформу при контакте"""
        if self.breakable:
            self.__level.remove_platform(self)

    def draw(self, surface: Surface) -> None:
        """Делает платформу с нужной текстуркой."""
        super().draw(surface)
        if self.__bonus:
            self.__bonus.draw(surface)
        if self.camera_rect.y + self.rect.height > config.YWIN:
            self.__level.remove_platform(self)


class Level(Singleton):
    """Класс для представления уровня."""

    def __init__(self):
        self.first = True
        self.platform_size = config.PLATFORM_SIZE
        self.max_platforms = config.MAX_PLATFORM_NUMBER
        self.distance_min = min(config.PLATFORM_DISTANCE_GAP)
        self.distance_max = max(config.PLATFORM_DISTANCE_GAP)
        self.bonus_platform_chance = config.BONUS_SPAWN_CHANCE
        self.breakable_platform_chance = config.BREAKABLE_PLATFORM_CHANCE

        self.__platforms = []
        self.__to_remove = []

        self.__base_platform = Platform(0, 0, *self.platform_size)

    @property
    def platforms(self) -> list:
        return self.__platforms

    async def _generation(self) -> None:
        nb_to_generate = self.max_platforms - len(self.__platforms)
        for _ in range(nb_to_generate):
            self.create_platform()
            self.first = False

    def create_platform(self) -> None:
        if self.__platforms:
            offset = randint(self.distance_min, self.distance_max)
            self.__platforms.append(Platform(
                randint(0, config.XWIN - self.platform_size[0]),  # X
                self.__platforms[-1].rect.y - offset,  # Y
                *self.platform_size,  # размер
                initial_bonus=chance(self.bonus_platform_chance),
                breakable=chance(self.breakable_platform_chance)))
        else:
            self.__platforms.append(self.__base_platform)

    def remove_platform(self, plt: Platform) -> bool:
        """Удаляет из уровня платформу"""
        if plt in self.__platforms:
            self.__to_remove.append(plt)
            return True
        return False

    def reset(self) -> None:
        self.__platforms = [self.__base_platform]

    def update(self) -> None:
        for platform in self.__to_remove:
            if platform in self.__platforms:
                self.__platforms.remove(platform)
        self.__to_remove = []
        asyncio.run(self._generation())  # асинхронная таска, в фоне генерирующая уровень

    def draw(self, surface: Surface) -> None:
        for platform in self.__platforms:
            platform.draw(surface)
