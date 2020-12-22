import pygame
import random
import sys
from pygame.locals import QUIT, K_SPACE, K_UP, K_LEFT, K_RIGHT, K_DOWN

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
        self.boulders = [Boulder(self) for _ in range(random.randint(2, 5))]
        self.all_sprites = pygame.sprite.Group((self.lander, ))
        self.all_sprites.add(self.boulders)
        self.all_sprites.add(self.moon)

    def handle_keys(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if keys[K_SPACE] or keys[K_UP]:
            self.lander.boost()
        elif keys[K_DOWN]:
            self.lander.fire_bomb()
        elif keys[K_LEFT]:
            self.lander.rotate_left()
        elif keys[K_RIGHT]:
            self.lander.rotate_right()

    def check_landing_and_collisions(self) -> bool:
        lander_status = self.lander.check_collisions()
        # TODO: Upgrade #5: Add code here to call bomb.check_collisions() for each bomb in self.lander.bombs
        if lander_status == 'LANDED':
            helpers.render_center_text(self.screen, "You landed successfully!", (0, 255, 0))
            return True
        elif lander_status == 'CRASHED':
            helpers.render_center_text(self.screen, "Kaboom! Your craft is destroyed.", (255, 0, 0))
            return True
        else:
            return False

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

    def __init__(self, gameobj: LunarLanderGame):
        super().__init__()
        self.image_normal, self.rect_normal = helpers.load_image('lander.jpg', colorkey=-1)
        self.image_boosting, self.rect_boosting = helpers.load_image('lander_flame.jpg', colorkey=-1)
        # TODO: Upgrade #4: There should be a line here to load the exploded lander image, following the above 2 lines.
        self.mass = 10
        self.orientation = 0.0  #
        self.rect_normal.topleft = ((gameobj.screen_width / 4), 20)  # The starting point.
        self.rect = self.rect_normal
        self.velocity = helpers.V(0.0, 0.0)  # Starting velocity.
        self.stopped = False  # Have we stopped?
        self.intact = True  # Is the ship still shipshape?
        self.fuel = 30  # Units of fuel
        self.boosting = 0  # Are we in "boost" mode? (show the flame graphic)
        self.game_object = gameobj
        self.bombs = []
        self.engine_power = 0.14  # The power of the engine.
        self.gravity_power = 0.05

    def update_image(self) -> None:
        """
        Update our image based on orientation and engine state of the craft.
        """
        img = self.select_image()
        center = self.rect_normal.center
        self.image = pygame.transform.rotate(img, -1 * self.orientation)
        self.rect_normal = self.image.get_rect(center=center)
        self.rect = self.rect_normal

    def select_image(self) -> pygame.Surface:
        """
        Chooses the correct image for each state of the lander.

        TODO: Upgrade #4: You can use logic branching to set the lunar lander explosion graphic here.
                          Be sure to change line 105 as well.

        :returns: Surface object that is the correct image
        """
        if self.boosting:
            return self.image_boosting
        elif not self.intact:
            return self.image_normal
        else:
            return self.image_normal

    def rotate_left(self, angle: float = 2.0) -> None:
        """
        Rotate the craft.
        """
        self.orientation -= angle

    def rotate_right(self, angle: float = 2.0) -> None:
        """
        Rotate the craft.
        """
        self.orientation += angle

    def boost(self) -> None:
        """
        Provide a boost to our craft's velocity in whatever orientation we're currently facing.
        """
        if self.fuel <= 0.0:
            return
        self.velocity += helpers.V(magnitude=self.engine_power, angle=self.orientation)
        self.fuel -= self.engine_power
        self.boosting = 3

    def fire_bomb(self):
        self.bombs.append(Bomb(self.game_object))
        self.game_object.all_sprites.add(self.bombs)

    def stop(self) -> None:
        """
        Stops the lunar lander.
        """
        self.velocity = helpers.V(0.0, 0.0)
        self.stopped = True

    def physics_update(self) -> None:
        """
        Updates the physics calculation.
        """
        if not self.stopped:
            self.velocity += helpers.V(magnitude=self.gravity_power, angle=180)

    def check_collisions(self) -> str:
        """
        Checks if any collisions have occurred between boulders, the moon surface, and the lander.

        TODO: Upgrade #1: check if the lunar lander has exited the screen
              Hint: you will need to use use self.game_object.screen.get_rect().contains(xxx) and check if
                    self.rect (which is the Rect object that represents the lunar lander) is in the screen.
                    Think about what should be passed into .contains() where xxx is.
                    See: http://www.pygame.org/docs/ref/rect.html#pygame.Rect.contains

        :return: The collision status of the lunar lander: 'LANDED', 'CRASHED', or 'FLYING'
        """
        has_hit_moon = pygame.sprite.collide_rect(self, self.game_object.moon)
        landed_vertically_and_slowly = (self.orientation < 8 or self.orientation > 352) and self.velocity.magnitude < 3
        has_hit_boulder = False
        for boulder in self.game_object.boulders:
            has_hit_boulder = has_hit_boulder or pygame.sprite.collide_circle(self, boulder)
        if has_hit_moon and landed_vertically_and_slowly:
            self.stop()
            return 'LANDED'
        elif has_hit_moon or has_hit_boulder:  # TODO: You can achieve Upgrade #1 by just modifying this line.
            self.intact = False
            self.stop()
            return 'CRASHED'
        else:
            return 'FLYING'

    def update(self) -> None:
        self.dirty = True
        self.physics_update()  # Iterate physics
        if self.boosting > 0:
            self.boosting -= 1  # Tick over engine time
        self.update_image()
        np = self.rect_normal.move(self.velocity.x, -1 * self.velocity.y)
        self.rect_normal = np

    def stats(self):
        return ' '.join((f"Position: [{self.rect_normal.top}, {self.rect_normal.left}]",
                         f"Velocity: {self.velocity.magnitude} at {self.velocity.angle} degrees",
                         f"Orientation: {self.orientation} degrees",
                         f"Fuel: {self.fuel} Status OK: [{self.intact}]"))


class Bomb(pygame.sprite.DirtySprite):
    def __init__(self, game_object: LunarLanderGame):
        super().__init__()
        self.game_object = game_object
        self.stopped = False
        self.velocity = helpers.V(0.0, 0.0)
        self.diameter = 2
        self.radius = self.diameter // 2
        self.x_pos, self.y_pos = self.game_object.lander.rect_normal.center
        self.image = pygame.Surface((self.diameter, self.diameter)).convert()
        self.image.fill((255, 255, 255, 128))
        pygame.draw.circle(self.image, (128, 0, 0), (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(self.x_pos, self.y_pos,
                                self.diameter, self.diameter)

    def update(self) -> None:
        if not self.stopped:
            self.velocity += helpers.V(magnitude=0.1, angle=180)
            self.rect = self.rect.move(self.velocity.x, -1 * self.velocity.y)

    def check_collisions(self) -> None:
        for boulder in self.game_object.boulders:
            if pygame.sprite.collide_circle(self, boulder):
                self.stopped = True
                self.game_object.all_sprites.remove(boulder)
                self.game_object.all_sprites.remove(self)
