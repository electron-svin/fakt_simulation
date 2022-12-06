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
        """
        self.screen = screen
        self.height = 100
        self.width = 20
        self.coord_cm = 0  # растояние вверх от центра ракеты до центра масс
        self.moment_of_inertia = 100000  # момент инерции относительно центра масс
        self.nozzle_angle = 0  # угол поворота сопла
        self.shell_mass = 1000
        self.max_fuel_mass = 500
        self.fuel_mass = self.max_fuel_mass
        self.engine_on = False
        self.mu = 10
        self.u = 4000
        self.angle = 0  # угол с вертикалью, положителен обход против часовой стрелки
        self.vx = 0
        self.vy = 0
        self.omega = 0 # угловая скорость вращения против часовой стрелки
        self.x = 0
        self.y = 6400000
        self.r = 30
        self.color = GREY
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
        force_x, force_y = [0, 0]
        if self.engine_on:
            force_x = - self.mu * self.u * math.sin(self.angle)  # при отклонении влево sin>0 -> force_x<0
            force_y = self.mu * self.u * math.cos(self.angle)  # без отклонения cos>0 -> force_y>0 (ось y инвертирована)
        return [force_x, force_y]

    def waste_fuel(self):
        """Тратит часть топлива каждый кадр, уменьшая fuel mass, выключает двигатель при отсутствии топлива"""
        if self.engine_on:
            self.fuel_mass -= self.mu / FPS
        if self.fuel_mass <= 0:
            self.engine_on = False


    def draw_fuel_tank(self, scale_factor):
        """Визуализирует бак прямоугольником в правом нижнем углу"""
        height = 200
        width = 40
        color = BLACK
        if self.fuel_mass > 0:
            color = (200 * (1 - self.fuel_mass / self.max_fuel_mass), 200 * (self.fuel_mass / self.max_fuel_mass), 0)
        remainder = height / self.max_fuel_mass * self.fuel_mass
        pygame.draw.rect(self.screen, BLACK, (WIDTH - width - 10, HEIGHT - height - 10, width, height))
        pygame.draw.rect(self.screen, color, (WIDTH - width - 10, HEIGHT - remainder - 10, width, remainder))

    def calculate_acceleration(self, force_x, force_y):
        """Изменяет x- и y- составляющие скорости ракеты за 1 кадр в соответствии с её полным ускорением"""
        self.vx += force_x / (self.shell_mass + self.fuel_mass) / FPS
        self.vy += force_y / (self.shell_mass + self.fuel_mass) / FPS

    def calculate_moment_of_inertia(self):
        self.moment_of_inertia = (self.shell_mass + self.fuel_mass) * (self.height ** 2 / 4 + self.coord_cm ** 2) / 6

    def calculate_angular_acceleration(self):
        if self.engine_on:
            moment_of_power = - self.mu * self.u * (self.height / 2 + self.coord_cm) * math.sin(self.nozzle_angle)
            epsilon = moment_of_power / self.moment_of_inertia
            self.omega += epsilon

    def draw(self, scale_factor):
        h = self.height / 2
        w = self.width / 2
        x1 = int(720 + (- h * math.sin(self.angle) + w * math.cos(self.angle)) * scale_factor)
        y1 = int(360 - (+ h * math.cos(self.angle) + w * math.sin(self.angle)) * scale_factor)
        x2 = int(720 + (- h * math.sin(self.angle) - w * math.cos(self.angle)) * scale_factor)
        y2 = int(360 - (+ h * math.cos(self.angle) - w * math.sin(self.angle)) * scale_factor)
        x3 = int(720 + (+ h * math.sin(self.angle) - w * math.cos(self.angle)) * scale_factor)
        y3 = int(360 - (- h * math.cos(self.angle) - w * math.sin(self.angle)) * scale_factor)
        x4 = int(720 + (+ h * math.sin(self.angle) + w * math.cos(self.angle)) * scale_factor)
        y4 = int(360 - (- h * math.cos(self.angle) + w * math.sin(self.angle)) * scale_factor)
        # pygame.draw.circle(self.screen, self.color, (720, 360), self.r * scale_factor)
        pygame.draw.polygon(self.screen, self.color, [[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        print(*[[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

        pygame.draw.circle(self.screen, self.color, (720, 360), 1)  # чтобы при удалении ракета не пропадала с экрана
        pygame.draw.circle(self.screen, self.color, (720 - 5 * math.sin(self.angle), 360 - 5 * math.cos(self.angle)), 1)

    def move(self):
        self.x += self.vx
        self.y += self.vy

        self.angle += self.omega


    def switch_engine(self, keys):
        """Включает/выключает двигатель при разовом нажатии на W/S"""
        if keys[self.up_key]:
            self.engine_on = True
        elif keys[self.down_key]:
            self.engine_on = False

    def turn(self, keys):
        """Включает/выключает двигатель при разовом нажатии на W/S"""
        self.nozzle_angle = 0
        if keys[self.left_key]:
            self.nozzle_angle = - 0.001
        if keys[self.right_key]:
            self.nozzle_angle = 0.001


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

    rocket.turn(pygame.key.get_pressed())
    rocket.switch_engine(pygame.key.get_pressed())

    thrust_force_x, thrust_force_y = 0, 0
    if rocket.fuel_mass > 0:
        thrust_force_x, thrust_force_y = rocket.calculate_thrust_force()
        rocket.waste_fuel()
    gravity_force_x, gravity_force_y = rocket.calculate_gravity(planet)

    rocket.calculate_acceleration(gravity_force_x+thrust_force_x, gravity_force_y+thrust_force_y)
    rocket.calculate_moment_of_inertia()
    rocket.calculate_angular_acceleration()
    rocket.move()

    screen.fill(WHITE)
    planet.draw(rocket)
    rocket.draw(planet.scale_factor)
    rocket.draw_fuel_tank(planet.scale_factor)
    planet.scale(pygame.key.get_pressed())

pygame.quit()
