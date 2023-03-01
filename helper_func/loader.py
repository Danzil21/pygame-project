import pygame
import settings
from helper_func.load_image import load_image


def draw_game_over_screen(screen, player_, bc, ov, best_score):
    max_score = player_.score_manager.get_score()

    game_over_text = settings.pixel_font.render("Game Over", True,
                                             pygame.Color('whitesmoke'))
    score_text = settings.pixel_font.render(f"Текущий рекрод: {'%.2f' % player_.score}", True,
                                   pygame.Color('whitesmoke'))
    max_score_text = settings.pixel_font.render(f"Лучший рекрод: {'%.2f' % max_score}", True,
                                       pygame.Color('whitesmoke'))

    screen.blit(bc, (0, 0))
    screen.blit(ov, (0, 0))
    screen.blit(game_over_text, (73, 100))
    screen.blit(max_score_text, (73, 220))
    screen.blit(score_text, (73, 255))
    if best_score:
        best_score_text = settings.pixel_font.render("Вы побили свой рекорд!", True, pygame.Color('whitesmoke'))
        screen.blit(best_score_text, (73, 180))


background = load_image('backgrounds\\background.jpg')
overlay_img = pygame.transform.scale(load_image
                                     ('backgrounds\\black_overlay.png'), (450, 700))  # Resolution
overlay_img.set_alpha(150)
player = load_image('game\\player.png')
platform = load_image('game\\platform.png')
platform_trampoline = load_image('game\\platform-trampoline.png')
platform_break = load_image('game\\break.png')
