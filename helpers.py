import os
from typing import Tuple, Union
import pygame as pg
from pygame.locals import RLEACCEL
import math
import pygame


def load_image(filename: str,
               filedir: str = 'assets/img/',
               colorkey: int = None) -> Tuple[Union[pg.Surface], Union[pg.Rect]]:
    """
    Loads an image and returns the converted pygame Surface and Rectangle objects

    :param filename: string of the image file to load (such as 'lander.jpg')
    :param filedir: optional string of the folder to pull from, defaults to 'assets/img/'
    :param colorkey: optional int to represent the color key to pull
    :return:
    """
    path = os.path.join(filedir, filename)
    the_image = pg.image.load(path).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = the_image.get_at((0, 0))
        the_image.set_colorkey(colorkey, RLEACCEL)
    return the_image, the_image.get_rect()


def load_sound(filename: str, filedir: str = 'assets/snd/') -> pg.mixer.Sound:
    """
    Loads a sound file and returns the converted pygame Sound object

    :param filename: string of the sound file to load (such as 'music.mp4')
    :param filedir: optional string of the folder to pull from, defaults to 'assets/snd/'
    :return:
    """
    if not pg.mixer:
        raise ValueError('Pygame sound mixer not installed properly')
    file = os.path.join(filedir, filename)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        raise RuntimeError(f'Warning, unable to load {file}')


def load_bgmusic(filename: str, filedir: str = 'assets/snd/') -> None:
    """
    Loads a sound file into the mixer

    :param filename: string of the image file to load (such as 'lander.jpg')
    :param filedir: optional string of the folder to pull from, defaults to 'assets/img/'
    """
    if not pg.mixer:
        raise ValueError('Pygame sound mixer not installed properly')
    file = os.path.join(filedir, filename)
    try:
        pg.mixer.init()
        pg.mixer.music.load(file)
    except pg.error:
        raise RuntimeError(f'Warning, unable to load {file}')


def render_center_text(surface, screen, txt, color):
    font2 = pygame.font.Font(None, 36)
    text = font2.render(txt, True, color)
    textpos = text.get_rect()
    textpos.centerx = screen.get_size()[0] // 2
    textpos.centery = screen.get_size()[1] // 2
    surface.blit(text, textpos)
    screen.blit(surface, (0, 0))


class V(object):
    """
    A simple class to keep track of vectors, including initializing
    from Cartesian and polar forms.
    """

    def __init__(self, x: float = 0, y: float = 0,
                 angle: float = None, magnitude: float = None):
        self.x = x
        self.y = y

        if angle is not None and magnitude is not None:
            self.x = magnitude * math.sin(math.radians(angle))
            self.y = magnitude * math.cos(math.radians(angle))

    @property
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def angle(self):
        if self.y == 0:
            if self.x > 0:
                return 90.0
            else:
                return 270.0
        if math.floor(self.x) == 0:
            if self.y < 0:
                return 180.0
        return math.degrees(math.atan(self.x / float(self.y)))

    def __add__(self, other):
        return V(x=(self.x + other.x), y=(self.y + other.y))

    def rotate(self, angle):
        c = math.cos(math.radians(angle))
        s = math.sin(math.radians(angle))
        self.x = self.x * c - self.y * s
        self.y = self.x * s + self.y * c

    def __str__(self):
        return "X: %.3d Y: %.3d Angle: %.3d degrees Magnitude: %.3d" % (self.x, self.y, self.angle, self.magnitude)
