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
        self.local = pygame.K_MINUS

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
        if keys[self.local]:
            self.scale_factor = 2


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
        self.color = (160, 160, 180)
        self.left_key = pygame.K_a
        self.right_key = pygame.K_d
        self.up_key = pygame.K_w
        self.down_key = pygame.K_s
        self.show_information = False

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

        xh3 = int(720 + (- (h + 15) * math.sin(self.angle) - (w - 2) * math.cos(self.angle)) * scale_factor)
        yh3 = int(360 - (+ (h + 15) * math.cos(self.angle) - (w - 2) * math.sin(self.angle)) * scale_factor)
        xh5 = int(720 + (- (h + 25) * math.sin(self.angle) + (w - 6) * math.cos(self.angle)) * scale_factor)
        yh5 = int(360 - (+ (h + 25) * math.cos(self.angle) + (w - 6) * math.sin(self.angle)) * scale_factor)
        xh4 = int(720 + (- (h + 25) * math.sin(self.angle) - (w - 6) * math.cos(self.angle)) * scale_factor)
        yh4 = int(360 - (+ (h + 25) * math.cos(self.angle) - (w - 6) * math.sin(self.angle)) * scale_factor)
        xh6 = int(720 + (- (h + 15) * math.sin(self.angle) + (w - 2) * math.cos(self.angle)) * scale_factor)
        yh6 = int(360 - (+ (h + 15) * math.cos(self.angle) + (w - 2) * math.sin(self.angle)) * scale_factor)

        pygame.draw.polygon(self.screen, self.color,
                            [[x1, y1], [x2, y2],
                             [x3, y3], [x4, y4]])
        pygame.draw.polygon(self.screen, self.color,
                            [[x1, y1], [x2, y2],
                             [xh3, yh3], [xh4, yh4],
                             [xh5, yh5], [xh6, yh6]])
        pygame.draw.circle(self.screen, self.color, (720, 360), 1)  # чтобы при удалении ракета не пропадала с экрана
        pygame.draw.circle(self.screen, self.color,
                           (720 - 5 * math.sin(self.angle),
                            360 - 5 * math.cos(self.angle)), 1)
        if self.show_information:
            pygame.draw.line(self.screen, BLACK, [720, 360],
                             [720 - 40 * math.sin(self.angle),
                              360 - 40 * math.cos(self.angle)], 2)
            pygame.draw.line(self.screen, RED, [720, 360],
                             [720 + 10 * math.sin(self.angle + 500 * self.nozzle_angle),
                              360 + 10 * math.cos(self.angle + 500 * self.nozzle_angle)], 2)

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

    def change_inf_mode(self, keys):  #FIXME: должно считывать разовое нажатие,
        if keys[pygame.K_q] and not self.show_information:
            self.show_information = True
        elif keys[pygame.K_q]:
            self.show_information = False

if __name__ == "__main__":
    print("This module is not for direct call!")