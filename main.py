import pygame

from singleton import Singleton
from models.camera import Camera
from models.player import Player
from models.level import Level
from models.score import Score
from helper_func import loader
import settings as config
from models.button import Button


class Game(Singleton):
    def __init__(self) -> None:

        self.__alive = True
        self.score_manager = Score()
        # Window / Render
        self.window = pygame.display.set_mode(config.DISPLAY, config.FLAGS)
        pygame.display.set_caption('Doodle Jump')
        self.clock = pygame.time.Clock()
        self.new_game_button = Button(75, 300, 300, 100, (75, 200, 90), "Сыграть еще раз", (0, 0, 0),
                                      config.pixel_font_large)
        self.new_game_button.hidden = True

        # Instances
        self.camera = Camera()
        self.lvl = Level()
        self.player = Player(
            config.PLAYER_IMG,  # COLOR
            (50, 50)
        )

        # User Interface
        self.score = 0
        self.score_txt = config.SMALL_FONT.render("0 m", 1, config.GRAY)
        self.score_pos = pygame.math.Vector2(10, 10)

        self.gameover_txt = config.pixel_font_large.render("GameOver", 1, config.GRAY)
        self.gameover_rect = self.gameover_txt.get_rect(
            center=(config.HALF_XWIN, config.HALF_YWIN))

    def close(self):
        self.__alive = False

    def reset(self):
        self.camera.reset()
        self.lvl.reset()
        self.player.reset()
        self.score_manager.load_score()

    def _event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.close()
                if event.key == pygame.K_RETURN and self.player.dead:
                    self.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.new_game_button.is_clicked():
                    self.new_game_button.hide(self.window)
                    self.new_game_button.hidden = True
                    self.reset()
            self.player.handle_event(event)

    def _update_loop(self):
        self.player.update()
        self.lvl.update()

        if not self.player.dead:
            self.camera.update(self.player.rect)
            self.score = -self.camera.state.y // 50
            self.score_txt = config.SMALL_FONT.render(
                str(self.score) + " m", 1, config.GRAY)

    def _render_loop(self):
        self.window.blit(loader.background, (0, 0))
        self.lvl.draw(self.window)
        self.player.draw(self.window)

        # User Interface
        if self.player.dead:
            is_best_score = self.score > int(self.score_manager.score)
            self.window.blit(self.gameover_txt, self.gameover_rect)  # gameover
            loader.draw_game_over_screen(self.window, self, loader.background, loader.overlay_img, is_best_score)
            self.new_game_button.draw(self.window)
            self.new_game_button.hidden = False
            if is_best_score:
                self.score_manager.save_best_score(self.score)
        self.window.blit(self.score_txt, self.score_pos)

        pygame.display.update()
        self.clock.tick(config.FPS)  # max loop/s

    def run(self):
        while self.__alive:
            self._event_loop()
            self._update_loop()
            self._render_loop()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
