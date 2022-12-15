import math
import pygame

FPS = 30
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
BRIGHT_BLUE = (185, 237, 255)
COSMIC = (23, 23, 23)

gravitational_constant = 6.67408E-11


class Planet:

    def __init__(self, screen, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = screen
        self.mass = 5.9742E24
        self.x = 0
        self.y = 0
        self.r = 6371 * 10 ** 3
        self.color = GREEN
        self.scale_factor = 2
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.local = pygame.K_MINUS
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.time = 0
        self.dT = 0.03
        self.dT_initial = 0.03
        self.time_scale_counter = 0
        self.time_factor = 1
        self.time_scale_array = [1, 2, 3, 5, 10, 50, 100, 200, 500, 1000]
        self.time_scale_index = 1
        self.r_atmosphere = 100_000
        self.map_mode = False
        self.change_mode_timer = 0
        self.change_mode_key = pygame.K_q
        self.scale_to_rocket = pygame.K_LSHIFT
        self.color_atmosphere = BRIGHT_BLUE
        self.start_position = (WIDTH / 2, HEIGHT / 2)
        self.center_map = (WIDTH / 2, HEIGHT / 2)
        self.mouse_pressed = False
        self.time_scale_to_rocket_counter = 0
        self.image_stars = pygame.image.load("picture\\stars.jpg")
        self.air_force_height = 40_000

    def draw(self, rocket):
        if self.map_mode:
            pygame.draw.circle(self.screen, self.color_atmosphere, (self.center_map[0], self.center_map[1]), (self.r + self.r_atmosphere) * self.scale_factor)
            pygame.draw.circle(self.screen, self.color, (self.center_map[0], self.center_map[1]), self.r * self.scale_factor)
        else:
            if rocket.x ** 2 + rocket.y ** 2 < (self.r + self.r_atmosphere)**2:
                self.screen.fill(BRIGHT_BLUE)
            else:
                self.screen.blit(self.image_stars, (0, 0))
            h = self.HEIGHT / 2 - (((rocket.x ** 2 + rocket.y ** 2) ** 0.5 - self.r) * self.scale_factor)
            if h > 0:
                pygame.draw.polygon(self.screen, self.color, [[0, self.HEIGHT - h], [self.WIDTH, self.HEIGHT - h], [self.WIDTH, self.HEIGHT], [0, self.HEIGHT]])

    def scale(self, keys, rocket):
        if self.map_mode and keys[self.up]:
            self.scale_factor *= 1.05
        if self.map_mode and keys[self.down]:
            self.scale_factor /= 1.05
        if self.time_scale_to_rocket_counter == 0 and self.map_mode and keys[self.scale_to_rocket]:
            self.scale_factor = 10**-4
            self.center_map = (self.WIDTH / 2 - rocket.x * self.scale_factor, self.HEIGHT / 2 + rocket.y * self.scale_factor)
            self.time_scale_to_rocket_counter = 15

    def move_screen(self, action, event):
        if action == "down":
            self.start_position = event.pos
            self.mouse_pressed = True
        if self.mouse_pressed and action == 'motion':
            change_position = event.rel
            self.center_map = (self.center_map[0] + change_position[0],
                               self.center_map[1] + change_position[1])
        if action == "up":
            self.mouse_pressed = False

    def time_scale(self, keys):
        if self.time_scale_counter == 0 and keys[self.left]:
            if self.time_scale_index > 0:
                self.time_scale_index -= 1
                self.dT = self.dT_initial * self.time_scale_array[self.time_scale_index]
                self.time_scale_counter = 5
        if self.time_scale_counter == 0 and keys[self.right]:
            if self.time_scale_index < len(self.time_scale_array) - 2:
                self.time_scale_index += 1
                self.dT = self.dT_initial * self.time_scale_array[self.time_scale_index]
                self.time_scale_counter = 5

    def time_scale_counter_timer(self):
        if self.time_scale_counter > 0:
            self.time_scale_counter -= 1

    def time_scale_to_rocket_counter_timer(self):
        if self.time_scale_to_rocket_counter > 0:
            self.time_scale_to_rocket_counter -= 1

    def change_mode(self, keys):
        if self.change_mode_timer == 0 and keys[self.change_mode_key]:
            self.map_mode = not self.map_mode
            self.change_mode_timer = 10
            if self.map_mode:
                self.scale_factor = 45 * 10**-6
                self.center_map = (self.WIDTH / 2, self.HEIGHT / 2)
            else:
                self.scale_factor = 2

    def change_mode_timer_count(self):
        if self.change_mode_timer > 0:
            self.change_mode_timer -= 1


class Stage:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = screen
        self.height = 70
        self.radius = 20
        self.moment_of_inertia = 5 * 10 ** 6  # момент инерции относительно центра масс
        self.nozzle_angle = 0  # угол поворота сопла
        self.shell_mass = 30_000
        self.max_fuel_mass = 270_000
        self.fuel_mass = self.max_fuel_mass
        self.engine_on = False
        self.mu = 1000
        self.u = 4000
        self.angle = 0  # угол с вертикалью, положителен обход против часовой стрелки
        self.vx = 0
        self.vy = 0
        self.omega = 0 # угловая скорость вращения против часовой стрелки
        self.x = 0
        self.y = 6371_000 + self.height / 2
        self.image_stage = pygame.image.load("picture\\saturn_v_stage_1.png")
        self.collision_point = [(0, -35), (-24.75, 35), (24.75, 35)]
        self.inside_atmosphere = True
        self.flame_animation_file = "picture\\flame\\flame_"
        self.explosion_animation_file = "picture\\explosion\\"
        self.flame_animation_count = 0
        self.number_of_flame_animation = 12
        self.dead = False
        self.explosion_animation_count = 0
        self.number_of_explosion_animation = 30
        self.explosion_now = False
        self.x_explosion_point = 0
        self.y_explosion_point = 0
        self.bottom = 120

    def explosion_start(self, x_point_collision, y_point_collision):
        if not self.dead:
            self.dead = True
            self.x_explosion_point = x_point_collision
            self.y_explosion_point = y_point_collision

    def explosion(self, planet):
        if self.dead and self.explosion_animation_count <= self.number_of_explosion_animation - 1:
            if not planet.map_mode:
                number = int(self.explosion_animation_count)
                animation_image = pygame.image.load(self.explosion_animation_file + str(number) + ".png", )
                animation_image = pygame.transform.scale(animation_image, (800, 600))
                animation_image_rect = animation_image.get_rect(center=(self.WIDTH / 2 + self.x_explosion_point, self.HEIGHT / 2 - self.y_explosion_point))
                self.screen.blit(animation_image, animation_image_rect)
            self.explosion_animation_count += 0.5

    def draw(self, rocket_surface, planet):
        '''if not self.dead and planet.map_mode:
            w = planet.center_map[0]
            h = planet.center_map[1]
            coordinate_array = (w + self.x * planet.scale_factor, h - self.y * planet.scale_factor)
            current_mark_image = pygame.transform.scale(self.image_mark, (
                15, 20))
            current_mark_image = pygame.transform.rotate(current_mark_image, self.angle * 180 / 3.14)
            current_mark_rect = current_mark_image.get_rect(center=coordinate_array)
            self.screen.blit(current_mark_image, current_mark_rect)
            pygame.draw.line(self.screen, RED, coordinate_array,
                             [coordinate_array[0] + 10 * math.sin(self.angle + 500 * self.nozzle_angle),
                              coordinate_array[1] + 10 * math.cos(self.angle + 500 * self.nozzle_angle)], 2)'''
        '''if not self.dead:
            if self.engine_on and self.fuel_mass > 0:
                number = int(self.flame_animation_count)
                animation_image = pygame.image.load(self.flame_animation_file + str(number) + ".png", )
                animation_image = pygame.transform.scale(animation_image, (200, 200))
                animation_image = pygame.transform.rotate(animation_image, self.angle * 180 / 3.14 + 180)
                x, y = basis_rotation(2, 110, -self.angle)
                animation_image_rect = animation_image.get_rect(center=(self.WIDTH / 2 + x, self.HEIGHT / 2 + y))
                self.screen.blit(animation_image, animation_image_rect)
                self.flame_animation_count += 0.5
                if self.flame_animation_count > self.number_of_flame_animation - 1:
                    self.flame_animation_count = 0'''
        current_stages_surface = pygame.transform.scale(self.image_stage, (self.radius * 2 * planet.scale_factor, self.height * planet.scale_factor))
        current_stages_surface_rect = current_stages_surface.get_rect(bottom = self.bottom)
        rocket_surface.blit(current_stages_surface, (0, 0))


class Rocket:
    def __init__(self, screen, WIDTH, HEIGHT, planet):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = screen
        self.moment_of_inertia = 5 * 10 ** 6  # момент инерции относительно центра масс
        self.nozzle_angle = 0  # угол поворота сопла
        self.shell_mass = 30_000
        self.max_fuel_mass = 270_000
        self.fuel_mass = self.max_fuel_mass
        self.engine_on = False
        self.mu = 1000
        self.u = 4000
        self.left_key = pygame.K_a
        self.right_key = pygame.K_d
        self.up_key = pygame.K_w
        self.down_key = pygame.K_s
        self.radius = 20
        self.stages = [Stage(screen, WIDTH, HEIGHT)]
        stage2 = Stage(self.screen, self.WIDTH, self.HEIGHT)
        stage2.height = 50
        stage2.bottom = 50
        stage2.image_stage = pygame.image.load("picture\\saturn_v_stage_2.png")
        self.stages.append(stage2)
        self.height = 120
        self.angle = 0  # угол с вертикалью, положителен обход против часовой стрелки
        self.vx = 0
        self.vy = 0
        self.omega = 0  # угловая скорость вращения против часовой стрелки
        self.x = 0
        self.y = 6371_000 + self.height / 2
        self.dead = False
        self.image_mark = pygame.image.load("picture\\rocket_mark.png")
        self.rocket_surface = pygame.Surface((self.radius * 2 * planet.scale_factor, self.height * planet.scale_factor), pygame.SRCALPHA, 32)

    def draw_fuel_tank(self):
        """Визуализирует бак прямоугольником в правом нижнем углу"""
        height = 200
        width = 40
        color = BLACK
        if self.fuel_mass > 0:
            color = (200 * (1 - self.fuel_mass / self.max_fuel_mass), 200 * (self.fuel_mass / self.max_fuel_mass), 0)
        remainder = height / self.max_fuel_mass * self.fuel_mass
        pygame.draw.rect(self.screen, BLACK, (self.WIDTH - width - 10, self.HEIGHT - height - 10, width, height))
        pygame.draw.rect(self.screen, color, (self.WIDTH - width - 10, self.HEIGHT - remainder - 10, width, remainder))

    def draw(self, planet):
        if not self.dead and planet.map_mode:
            w = planet.center_map[0]
            h = planet.center_map[1]
            coordinate_array = (w + self.x * planet.scale_factor, h - self.y * planet.scale_factor)
            current_mark_image = pygame.transform.scale(self.image_mark, (
                15, 20))
            current_mark_image = pygame.transform.rotate(current_mark_image, self.angle * 180 / 3.14)
            current_mark_rect = current_mark_image.get_rect(center=coordinate_array)
            self.screen.blit(current_mark_image, current_mark_rect)
            pygame.draw.line(self.screen, RED, coordinate_array,
                             [coordinate_array[0] + 10 * math.sin(self.angle + 500 * self.nozzle_angle),
                              coordinate_array[1] + 10 * math.cos(self.angle + 500 * self.nozzle_angle)], 2)
        elif not self.dead:
            '''if self.engine_on and self.fuel_mass > 0:
                number = int(self.flame_animation_count)
                animation_image = pygame.image.load(self.flame_animation_file + str(number) + ".png", )
                animation_image = pygame.transform.scale(animation_image, (200, 200))
                animation_image = pygame.transform.rotate(animation_image, self.angle * 180 / 3.14 + 180)
                x, y = basis_rotation(2, 110, -self.angle)
                animation_image_rect = animation_image.get_rect(center=(self.WIDTH / 2 + x, self.HEIGHT / 2 + y))
                self.screen.blit(animation_image, animation_image_rect)
                self.flame_animation_count += 0.5
                if self.flame_animation_count > self.number_of_flame_animation - 1:
                    self.flame_animation_count = 0'''
            current_rocket_surface = self.rocket_surface
            self.stages[0].draw(self.rocket_surface, planet)
            self.stages[1].draw(self.rocket_surface, planet)
            current_rocket_surface = pygame.transform.rotate(current_rocket_surface, self.angle * 180 / 3.14)
            current_rocket_surface_rect = current_rocket_surface.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
            self.screen.blit(current_rocket_surface, current_rocket_surface_rect)

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


def basis_rotation(x, y, angle):
    return x * math.cos(angle) - y * math.sin(angle), x * math.sin(angle) + y * math.cos(angle)


if __name__ == "__main__":
    print("This module is not for direct call!")