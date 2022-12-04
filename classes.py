import math
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

gravitational_constant = 6.67408E-11


class Planet:

    def __init__(self, screen):
        self.screen = screen
        self.mass = 5.9742E24
        self.x = 0
        self.y = 0
        self.r = 6400 * 10 ** 3
        self.interaction_r = 6400 * 10 ** 6
        self.color = GREEN
        self.scale_factor = 1
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN

    def draw(self, rocket):
        pygame.draw.circle(self.screen, self.color,
                           (720 + (-rocket.x + self.x) * self.scale_factor,
                            360 + (rocket.y - self.y) * self.scale_factor),
                           self.r * self.scale_factor)


    def scale(self, keys):
        if keys[self.up]:
            self.scale_factor *= 1.05
        if keys[self.down]:
            self.scale_factor /= 1.05


class Rocket:

    def __init__(self, screen):
        """Target class constructor

        :param screen: pygame screen
        :param gun: tank's gun
        """
        self.screen = screen
        self.shell_mass = 1000
        self.fuel_mass = 5000
        self.mu = 100
        self.u = 2000
        self.angle = 0  # угол с вертикалью, положительен обход против часовой стрелки
        self.vx = 0
        self.vy = 0
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

    def calculate_gravity(self, obj):
        """Возвращает массив из x- и y- составляющих силы притяжения ракеты к объекту obj"""
        distance = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5
        force_x = gravitational_constant * (self.shell_mass + self.fuel_mass) * obj.mass * (obj.x - self.x) / (distance ** 3)
        force_y = gravitational_constant * (self.shell_mass + self.fuel_mass) * obj.mass * (obj.y - self.y) / (distance ** 3)
        return [force_x, force_y]

    def calculate_thrust_force(self):
        """Возвращает массив из x- и y- составляющих силы реактивной тяги ракеты"""
        force_x = - self.mu * self.u * math.sin(self.angle)  # при отклонении влево sin>0 -> force_x<0
        force_y = self.mu * self.u * math.cos(self.angle)  # без отклонения cos>0 -> force_y>0 (ось y инвертирована)
        self.fuel_mass
        return [force_x, force_y]

    def calculate_acceleration(self, force_x, force_y):
        """Изменяет x- и y- составляющие скорости ракеты за 1 кадр в соответствии с её полным ускорением"""
        self.vx += force_x / (self.shell_mass + self.fuel_mass) / FPS
        self.vy += force_y / (self.shell_mass + self.fuel_mass) / FPS

    def waste_fuel(self):
        self.fuel_mass -= self.mu / FPS

    def draw(self, scale_factor):
        pygame.draw.circle(self.screen, self.color, (720, 360), self.r * scale_factor)
        pygame.draw.circle(self.screen, self.color, (720, 360), 1)  # чтобы при удалении ракета не пропадала с экрана

    def move(self):
        self.x += self.vx
        self.y += self.vy


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

    thrust_force_x, thrust_force_y = 0, 0
    if rocket.fuel_mass > 0:
        thrust_force_x, thrust_force_y = rocket.calculate_thrust_force()
        rocket.waste_fuel()
    gravity_force_x, gravity_force_y = rocket.calculate_gravity(planet)
    rocket.calculate_acceleration(gravity_force_x+thrust_force_x, gravity_force_y+thrust_force_y)
    rocket.move()

    screen.fill(WHITE)
    rocket.draw(planet.scale_factor)
    planet.draw(rocket)
    planet.scale(pygame.key.get_pressed())

pygame.quit()
