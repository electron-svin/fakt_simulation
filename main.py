import pygame
from pygame.draw import *

from model import *
from classes import *

FPS = 30
dt = 0.0333333

WIDTH = 1440
HEIGHT = 720


def main():
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
            thrust_force_x, thrust_force_y = calculate_thrust_force(rocket)
            waste_fuel(rocket, dt)
        gravity_force_x, gravity_force_y = calculate_gravity(rocket, planet)

        calculate_acceleration(rocket, gravity_force_x + thrust_force_x, gravity_force_y + thrust_force_y, dt)
        calculate_moment_of_inertia(rocket)
        calculate_angular_acceleration(rocket)
        move(rocket)

        screen.fill(WHITE)
        planet.draw(rocket)
        rocket.change_inf_mode(pygame.key.get_pressed())
        rocket.draw(planet.scale_factor)
        rocket.draw_fuel_tank(planet.scale_factor)
        planet.scale(pygame.key.get_pressed())

    pygame.quit()

if __name__ == "__main__":
    main()

