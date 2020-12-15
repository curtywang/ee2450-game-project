#!/usr/bin/env python

"""
EE 2450 Final Project

This game is basically a template for a lunar lander version with asteroids.
It is your choice to make the following upgrades to the game.
A minimum of two upgrades are needed for a C grade.
Three upgrades are needed for a B grade.
To obtain an A grade, you must develop your own upgrade and implement it.

You can make any of the upgrades that need to be made to this game:
1. Making it so going off-screen causes the lunar lander to crash
     See check_collisions() in objects.py: Lines 193 and 209
2. A fantastic soundtrack
     See main() in main.py: Line 44
3. Retry on death instead of just quitting
     See main() in main.py: Line 56
4. Some fancier explosion graphics
     See Lander() class in objects.py: Lines 108 and 137
5. Bomb firing down the bottom (press DOWN key) to destroy asteroids
     See check_landing_and_collisions in objects.py: Line 50

To implement these upgrades, simply find the relevant TODO and add your code!
The TODO will be sprinkled between this file, helpers.py, and objects.py.

Your code may or may not depends on something in helpers.py, so be sure to look
at that too!

"""

import sys
import time
from objects import *


def main(screen_width: int = 1024, screen_height: int = 600):
    pygame.init()
    fps_clock = pygame.time.Clock()
    """
    TODO: Upgrade #2: Play a fantastic soundtrack for this by calling helpers.load_bgmusic() properly here
                      Then, you can call pygame.mixer.music.play() with the proper argument to play the music.
                      Put the calls here, before the LunarLanderGame object is created.
                      See: https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.play
    """
    gameobj = LunarLanderGame(screen_width, screen_height)
    while True:  # This is the main game loop -- it MUST be run forever.
        gameobj.handle_keys()
        gameobj.render_stats_text()
        gameobj.update_sprites()
        restart_game = gameobj.check_landing_and_collisions()
        """
        TODO: Upgrade #3: What will you add here to restart the game instead of just dying?
              Hint: you can recreate the LunarLanderGame gameobj object to reset everything.        
        """

        # DO NOT MODIFY BELOW HERE #
        pygame.display.flip()
        pygame.display.update()
        fps_clock.tick(60)


if __name__ == '__main__':
    main()
