import pygame
from pygame.draw import *

FPS = 30

WIDTH = 1440
HEIGHT = 720

GREY = 0x696969
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D


class Rocket:

    def __init__(self, screen):
        """Target class constructor

        :param screen: pygame screen
        :param gun: tank's gun
        """
        self.screen = screen
        self.vx = 10
        self.vy = 10
        self.x = 0
        self.y = 6400*10**3
        self.r = 30
        self.color = BLUE
        self.left_key = pygame.K_a
        self.right_key = pygame.K_d
        self.up_key = pygame.K_w
        self.down_key = pygame.K_s
        self.fire_key = pygame.K_e
        self.change_key = pygame.K_q

    def draw(self, scale_factor):
        pygame.draw.circle(self.screen, self.color, (720, 360), self.r * scale_factor)

    def move(self, keys):

        if keys[self.left_key]:
            self.x -= self.vx
        if keys[self.right_key]:
            self.x += self.vx
        if keys[self.up_key]:
            self.y += self.vy
        if keys[self.down_key]:
            self.y -= self.vy

class Planet:

    def __init__(self, screen):

        self.screen = screen
        self.x = 0
        self.y = 0
        self.r = 6400*10**3
        self.color = GREEN
        self.scale_factor = 1
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN

    def draw(self, rocket):
        pygame.draw.circle(self.screen, self.color,
                           (720 + (-rocket.x + self.x) * self.scale_factor ,
                            360 + (rocket.y - self.y) * self.scale_factor),
                           self.r * self.scale_factor)

    def scale(self, keys):
        if keys[self.up]:
            self.scale_factor *= 1.05
        if keys[self.down]:
            self.scale_factor /= 1.05



screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False

rocket = Rocket(screen)
planet = Planet(screen)

while not finished:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
    screen.fill(WHITE)
    rocket.draw(planet.scale_factor)
    planet.draw(rocket)
    planet.scale(pygame.key.get_pressed())
    rocket.move(pygame.key.get_pressed())
pygame.quit()