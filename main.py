#!/usr/bin/env python

"""
EE 2450 Final Project

This game is basically a template for a lunar lander version with asteroids.
It is your choice to make the following upgrades to the game.
A minimum of two upgrades are needed for a C grade.
Three upgrades are needed for a B grade.
To obtain an A grade, you must develop your own upgrade and implement it.

Upgrades that need to be made to this game:
1. Adding a prettier picture for the asteroids
2. Laser firing down the bottom to destroy asteroids
3. A fantastic soundtrack
4. Retry on death instead of just quitting
5. Some fancier explosion graphics
6. Difficulty level selection (changes amount of fuel allowed and gravity)

To implement these upgrades, simply find the relevant TODO and add your code!

The original code is in example_lunarlander.py, in case you need the original code.

Your code may or may not depends on something in helpers.py, so be sure to look
at that too!


"""

import sys
import time
from objects import *


def main(screen_width: int = 1024, screen_height: int = 600):
    pygame.init()
    fps_clock = pygame.time.Clock()
    gameobj = LunarLanderGame(screen_width, screen_height)
    while True:  # main game loop
        gameobj.handle_keys()
        gameobj.render_stats_text()
        gameobj.update_sprites()
        gameobj.check_landing_and_collisions()

        # DO NOT MODIFY BELOW HERE #
        pygame.display.flip()
        pygame.display.update()
        fps_clock.tick(60)


if __name__ == '__main__':
    main()
