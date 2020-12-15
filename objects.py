import pygame
import random
import math


import helpers


"""
hello

TODO: collision when exit screen
"""


class GameSettings(object):
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lander = None
        self.moon = None
        self.sprites = None
        self.boulders = None
        self.allsprites = None

    def setup_game(self):
        self.lander = Lander(self)
        self.moon = Moon(self)
        self.sprites = [self.lander]
        self.boulders = [Boulder(self) for i in range(random.randint(2, 5))]
        self.sprites.extend(self.boulders)
        self.sprites.append(self.moon)
        self.allsprites = pygame.sprite.RenderPlain(self.sprites)
        # return self.lander, self.moon, self.boulders,


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


class Lander(pygame.sprite.DirtySprite):
    """
    Our intrepid lunar lander!
    """

    def __init__(self, settings: GameSettings):
        super().__init__()
        self.image, self.rect = helpers.load_image('lander.jpg', colorkey=-1)
        self.original = self.image
        self.original_flame, self.flame_rect = helpers.load_image('lander_flame.jpg', colorkey=-1)
        self.mass = 10
        self.orientation = 0.0  #
        self.rect.topleft = ((settings.screen_width / 2), 20)  # The starting point.
        self.velocity = V(0.0, 0.0)  # Starting velocity.
        self.landed = False  # Have we landed yet?
        self.intact = True  # Is the ship still shipshape?
        self.fuel = 10  # Units of fuel
        self.boosting = 0  # Are we in "boost" mode? (show the flame graphic)
        self.game_settings = settings
        self.engine_power = 0.1  # The power of the engine.
        self.falling_power = 0.05
        # return super(pygame.sprite.DirtySprite, self).__init__()

    def update_image(self):
        """
        Update our image based on orientation and engine state of the craft.
        """
        img = self.original_flame if self.boosting else self.original
        center = self.rect.center
        self.image = pygame.transform.rotate(img, -1 * self.orientation)
        self.rect = self.image.get_rect(center=center)

    def rotate(self, angle):
        """
        Rotate the craft.
        """
        self.orientation += angle

    def boost(self):
        """
        Provide a boost to our craft's velocity in whatever orientation we're currently facing.
        """
        if not self.fuel:
            return
        self.velocity += V(magnitude=self.engine_power, angle=self.orientation)
        self.fuel -= self.engine_power
        if self.landed:
            self.landed = False
            np = self.rect.move(0, -5)
            self.rect = np
        self.boosting = 3

    def physics_update(self):
        if not self.landed:
            self.velocity += V(magnitude=self.falling_power, angle=180)

    def ok_to_land(self):
        return (self.orientation < 10 or self.orientation > 350) and self.velocity.magnitude < 5

    def check_landed(self, surface):
        if self.landed:
            return
        if hasattr(surface, "radius"):
            collision = pygame.sprite.collide_circle(self, surface)
        else:
            collision = pygame.sprite.collide_rect(self, surface)
        if collision:
            self.landed = True
            self.intact = self.ok_to_land() and surface.landing_ok
            self.velocity = V(0.0, 0.0)  # In any case, we stop moving.

    def update(self):
        self.physics_update()  # Iterate physics
        if self.boosting:
            self.boosting -= 1  # Tick over engine time
        self.update_image()
        np = self.rect.move(self.velocity.x, -1 * self.velocity.y)
        self.rect = np
        self.dirty = True

    def explode(self, screen):
        for i in range(random.randint(20, 40)):
            pygame.draw.line(screen,
                             (random.randint(190, 255),
                              random.randint(0, 100),
                              random.randint(0, 100)),
                             self.rect.center,
                             (random.randint(0, self.game_settings.screen_width),
                              random.randint(0, self.game_settings.screen_height)),
                             random.randint(1, 3))

    def stats(self):
        return "Position: [%.2d,%.2d] Velocity: %.2f m/s at %.3d degrees Orientation: %.3d degrees  Fuel: %d Status: [%s]" % (
            self.rect.top, self.rect.left, self.velocity.magnitude, self.velocity.angle, self.orientation, self.fuel, (
                "Crashed" if not self.intact else (
                    "Landed" if self.landed else ("OK to Land" if self.ok_to_land() else "Not OK"))))


class Moon(pygame.sprite.DirtySprite):
    def __init__(self, settings: GameSettings):
        super().__init__()
        self.width = settings.screen_width + 20
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(-10, settings.screen_height - 20, settings.screen_width + 20, 20)
        self.landing_ok = True
        # return super(pygame.sprite.DirtySprite, self).__init__()


class Boulder(pygame.sprite.DirtySprite):
    def __init__(self, settings: GameSettings):
        super().__init__()
        self.diameter = random.randint(2, 300)
        self.radius = self.diameter / 2
        self.x_pos = random.randint(0, settings.screen_width)
        self.image = pygame.Surface((self.diameter, self.diameter))
        # self.image.fill((255,255,255,128))
        pygame.draw.circle(self.image, (128, 128, 128), (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(self.x_pos, settings.screen_height - (20 + self.radius),
                                self.diameter, self.diameter)
        self.image = self.image.convert()
        self.landing_ok = False
        # self.dirty = False
        # return super(pygame.sprite.DirtySprite, self).__init__()