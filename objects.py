import pygame
import random
import sys
import math
from pygame.locals import QUIT, K_r, K_SPACE, K_UP, K_LEFT, K_RIGHT

import helpers


"""
TODO: collision when exit screen
"""


class LunarLanderGame(object):
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 14)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.surface.fill((255, 255, 255))
        pygame.key.set_repeat(1, 1)

        # draw sprites and objects #
        self.lander = Lander(self)
        self.moon = Moon(self)
        self.boulders = [Boulder(self) for i in range(random.randint(2, 5))]
        self.sprites = [self.lander, self.moon]
        self.sprites.extend(self.boulders)
        self.all_sprites = pygame.sprite.RenderPlain(self.sprites)

    def handle_keys(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if keys[K_SPACE] or keys[K_UP]:
            self.lander.boost()
        elif keys[K_LEFT]:
            self.lander.rotate_left()
        elif keys[K_RIGHT]:
            self.lander.rotate_right()

    def check_landing_and_collisions(self):
        # TODO: what will you modify here to restart the game instead of just dying?
        collision_occurred = False
        for boulder in self.boulders:
            collision_occurred = collision_occurred or self.lander.has_collided(boulder)
        has_landed = self.lander.has_landed(self.moon)
        if has_landed and self.lander.has_landed_safely():
            helpers.render_center_text(self.surface, self.screen, "You landed successfully!", (0, 255, 0))
            self.lander.stop()
        elif collision_occurred or has_landed:
            helpers.render_center_text(self.surface, self.screen, "Kaboom! Your craft is destroyed.", (255, 0, 0))
            self.lander.explode(self.screen)
            self.lander.stop()

    def render_stats_text(self):
        stats_text = self.font.render(self.lander.stats(), True, (10, 10, 10))
        stats_pos = stats_text.get_rect()
        stats_pos.centerx = self.screen_width // 2
        self.surface.blit(stats_text, stats_pos)
        self.screen.blit(self.surface, (0, 0))

    def update_sprites(self):
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        self.surface.fill((255, 255, 255))


class Moon(pygame.sprite.DirtySprite):
    def __init__(self, settings: LunarLanderGame):
        super().__init__()
        self.height = 20
        self.landing_allowed = True
        self.width = settings.screen_width
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(0, settings.screen_height - self.height,
                                settings.screen_width, self.height)


class Boulder(pygame.sprite.DirtySprite):
    def __init__(self, settings: LunarLanderGame):
        super().__init__()
        self.landing_allowed = False
        self.diameter = random.randint(2, 120)
        self.radius = self.diameter / 2
        self.x_pos = random.randint(0, settings.screen_width)  # random placement on screen

        self.image = pygame.Surface((self.diameter, self.diameter)).convert()
        self.image.fill((255,255,255,128))
        pygame.draw.circle(self.image, (128, 128, 128), (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(self.x_pos, settings.screen_height - (20 + self.radius),
                                self.diameter, self.diameter)


class Lander(pygame.sprite.DirtySprite):
    """
    Our intrepid lunar lander!
    """

    def __init__(self, settings: LunarLanderGame):
        super().__init__()
        self.image, self.rect = helpers.load_image('lander.jpg', colorkey=-1)
        self.original = self.image
        self.original_flame, self.flame_rect = helpers.load_image('lander_flame.jpg', colorkey=-1)
        self.mass = 10
        self.orientation = 0.0  #
        self.rect.topleft = ((settings.screen_width / 4), 20)  # The starting point.
        self.velocity = helpers.V(0.0, 0.0)  # Starting velocity.
        self.stopped = False  # Have we stopped?
        self.intact = True  # Is the ship still shipshape?
        self.fuel = 30  # Units of fuel
        self.boosting = 0  # Are we in "boost" mode? (show the flame graphic)
        self.game_settings = settings
        self.engine_power = 0.14  # The power of the engine.
        self.gravity_power = 0.05
        # return super(pygame.sprite.DirtySprite, self).__init__()

    def update_image(self):
        """
        Update our image based on orientation and engine state of the craft.
        """
        img = self.original_flame if self.boosting else self.original  # TODO: upgrade 5
        center = self.rect.center
        self.image = pygame.transform.rotate(img, -1 * self.orientation)
        self.rect = self.image.get_rect(center=center)

    def select_image(self):
        """
        Chooses the correct image for each state of the lander.
        TODO: upgrade possibility 5 should be modified here!
        """
        if self.boosting:
            return self.original_flame
        elif not self.intact:
            return self.original
        else:
            return self.original

    def rotate_left(self, angle: float = 2.0):
        """
        Rotate the craft.
        """
        self.orientation -= angle

    def rotate_right(self, angle: float = 2.0):
        """
        Rotate the craft.
        """
        self.orientation += angle

    def boost(self):
        """
        Provide a boost to our craft's velocity in whatever orientation we're currently facing.
        """
        if self.fuel <= 0.0:
            return
        self.velocity += helpers.V(magnitude=self.engine_power, angle=self.orientation)
        self.fuel -= self.engine_power
        self.boosting = 3

    def stop(self):
        self.velocity = helpers.V(0.0, 0.0)
        self.stopped = True

    def physics_update(self):
        if not self.stopped:
            self.velocity += helpers.V(magnitude=self.gravity_power, angle=180)

    # TODO: make a check_collisions(self, boulder_list, moon_surface, screen) function to replace the below


    def has_landed_safely(self) -> bool:
        self.intact = (self.orientation < 8 or self.orientation > 352) and self.velocity.magnitude < 3
        return self.intact  # TODO: fix this

    def has_collided(self, boulder_surface: Boulder) -> bool:
        if self.intact:
            self.intact = not pygame.sprite.collide_circle(self, boulder_surface)
        return self.intact

    def has_landed(self, moon_surface: Moon):
        return pygame.sprite.collide_rect(self, moon_surface)

    # TODO: replace the above

    def update(self):
        self.dirty = True
        self.physics_update()  # Iterate physics
        if self.boosting > 0:
            self.boosting -= 1  # Tick over engine time
        self.update_image()
        np = self.rect.move(self.velocity.x, -1 * self.velocity.y)
        self.rect = np

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
        return ' '.join((f"Position: [{self.rect.top}, {self.rect.left}]",
                         f"Velocity: {self.velocity.magnitude} at {self.velocity.angle} degrees",
                         f"Orientation: {self.orientation} degrees",
                         f"Fuel: {self.fuel} Status OK: [{self.intact}]"))
