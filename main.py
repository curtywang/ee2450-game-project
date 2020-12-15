#!/usr/bin/env python

""" EE 2450 Final Project

This game is basically a template for a lunar lander version with asteroids.
It is your choice to make the following upgrades to the game.
A minimum of two upgrades are needed for a C grade.
Three upgrades are needed for a B grade.
To obtain an A grade, you must develop your own upgrade and implement it.

Upgrades that need to be made to this game:
1. Asteroids move randomly on the screen.
2. Laser from
3. A fantastic soundtrack
4. Retry on death instead of just quitting
5. Lives (rather than just 1)
6. Some fancier explosion graphics

To


"""

import os
import pygame as pg
import random

import objects
import helpers

# game constants
MAX_SHOTS = 2  # most player bullets onscreen
ALIEN_ODDS = 22  # chances a new alien appears
BOMB_ODDS = 60  # chances a new bomb will drop
ALIEN_RELOAD = 12  # frames between new aliens
SCREENRECT = pg.Rect(0, 0, 640, 480)
SCORE = 0
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


# our game object class
class GameObject:
    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)

    def move(self):
        self.pos = self.pos.move(self.speed, 0)
        if self.pos.right > 600:
            self.pos.left = 0


# here's the full code
def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))

    player = helpers.load_image("player1.gif", MAIN_DIR)
    background = helpers.load_image("liquid.bmp", MAIN_DIR)

    # scale the background image so that it fills the window and
    #   successfully overwrites the old sprite position.
    background = pg.transform.scale2x(background)
    background = pg.transform.scale2x(background)

    screen.blit(background, (0, 0))

    objects = []
    for x in range(10):
        o = GameObject(player, x * 40, x)
        objects.append(o)

    while 1:
        for event in pg.event.get():
            if event.type in (pg.QUIT, pg.KEYDOWN):
                return

        for o in objects:
            screen.blit(background, o.pos, o.pos)
        for o in objects:
            o.move()
            screen.blit(o.image, o.pos)

        pg.display.update()


if __name__ == "__main__":
    main()