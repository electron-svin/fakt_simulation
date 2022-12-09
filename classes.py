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
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.time = 0
        self.dT = 0.03

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

    def time_scale(self, keys):
        if keys[self.left] and self.dT > 0.03:
            self.dT /= 1.05
        if keys[self.right]:
            self.dT *= 1.2

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
        self.change_key = pygame.K_q
        self.show_information = False
        self.change_info_timer = 0
        self.image = pygame.image.load("picture\\rocket.png")

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


    def draw(self, scale_factor):
        current_image = pygame.transform.scale(self.image, (int(200 * scale_factor), int(200 * scale_factor)))
        current_image = pygame.transform.rotate(current_image, self.angle * 180/3.14)
        current_image_rect = current_image.get_rect(center=(720, 360))
        self.screen.blit(current_image, current_image_rect)

        if self.show_information:
            pygame.draw.line(self.screen, BLACK, [720, 360],
                             [720 - 40 * math.sin(self.angle),
                              360 - 40 * math.cos(self.angle)], 2)
            pygame.draw.line(self.screen, RED, [720, 360],
                             [720 + 10 * math.sin(self.angle + 500 * self.nozzle_angle),
                              360 + 10 * math.cos(self.angle + 500 * self.nozzle_angle)], 2)


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

    def change_inf_mode(self, keys):
        if self.change_info_timer == 0 and keys[self.change_key]:
            self.show_information = not(self.show_information)
            self.change_info_timer = 5

    def change_info_timer_count(self):
        if self.change_info_timer > 0:
            self.change_info_timer -= 1


if __name__ == "__main__":
    print("This module is not for direct call!")