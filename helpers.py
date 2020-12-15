import os
from typing import Tuple, Union, Any
import pygame as pg
from pygame.locals import RLEACCEL


# quick function to load an image
def load_image(filename: str, filedir: str = 'assets/img/', colorkey=None) -> Tuple[Union[pg.Surface], Union[pg.Rect]]:
    path = os.path.join(filedir, filename)
    the_image = pg.image.load(path).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = the_image.get_at((0, 0))
        the_image.set_colorkey(colorkey, RLEACCEL)
    return the_image, the_image.get_rect()


def load_sound(filename: str, main_dir: str = 'assets/snd/') -> pg.mixer.Sound:
    """ because pygame can be be compiled without mixer.
    """
    if not pg.mixer:
        raise ValueError('Pygame sound mixer not installed properly')
    file = os.path.join(main_dir, filename)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        raise RuntimeError(f'Warning, unable to load {filename}')
