#!/usr/bin/env python
import sys
import time
from pygame.locals import QUIT, K_r, K_SPACE, K_UP, K_LEFT, K_RIGHT
from objects import *


def render_center_text(surface, screen, txt, color, settings: GameSettings):
    font2 = pygame.font.Font(None, 36)
    text = font2.render(txt, True, color)
    textpos = text.get_rect()
    textpos.centerx = settings.screen_width // 2
    textpos.centery = settings.screen_height // 2
    surface.blit(text, textpos)
    screen.blit(surface, (0, 0))


def main(screen_width: int = 1024, screen_height: int = 600):
    FPS = 80
    pygame.init()
    fps_clock = pygame.time.Clock()
    gameobj = GameSettings(screen_width, screen_height)
    screen = pygame.display.set_mode((gameobj.screen_width, gameobj.screen_height), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill((255, 255, 255))
    pygame.key.set_repeat(1, 1)
    gameobj.setup_game()
    font = pygame.font.Font(None, 14)

    while True:
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if keys[K_r]:
            gameobj.setup_game()
        elif keys[K_SPACE] or keys[K_UP]:
            gameobj.lander.boost()
        elif keys[K_LEFT]:
            gameobj.lander.rotate(-5)
        elif keys[K_RIGHT]:
            gameobj.lander.rotate(5)

        gameobj.lander.check_landed(gameobj.moon)
        for boulder in gameobj.boulders:
            gameobj.lander.check_landed(boulder)

        surface.fill((255, 255, 255))

        text = font.render(gameobj.lander.stats(), True, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = gameobj.screen_width // 2
        surface.blit(text, textpos)
        screen.blit(surface, (0, 0))
        gameobj.allsprites.update()
        gameobj.allsprites.draw(screen)

        if gameobj.lander.landed:
            if not gameobj.lander.intact:
                gameobj.lander.explode(screen)
                render_center_text(surface, screen, "Kaboom! Your craft is destroyed.", (255, 0, 0), gameobj)
            else:
                render_center_text(surface, screen, "You landed successfully!", (0, 255, 0), gameobj)
            pygame.display.flip()
            pygame.display.update()
            time.sleep(8)
            gameobj.setup_game()
        else:
            pygame.display.flip()
            pygame.display.update()

        fps_clock.tick(FPS)  # and tick the clock.


if __name__ == '__main__':
    main()
