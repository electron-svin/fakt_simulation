import pygame
from pygame.draw import *

from model import *
from classes import *

FPS = 60

WIDTH = 1440
HEIGHT = 720


def text_score(text, planet, rocket):
    txt = text.render('time: ' + f"{planet.time:.{1}f}" + " s", True, (139, 0, 255))
    planet.screen.blit(txt, (20, 30))
    txt = text.render('height: ' + f"{(rocket.x**2 + rocket.y**2)**0.5  - 6400_035:.{1}f}" + " м", True, (139, 0, 255))
    planet.screen.blit(txt, (20, 50))
    txt = text.render('time_scale: ' + f"{(planet.time_scale_array[planet.time_scale_index]):.{1}f}", True,
                      (139, 0, 255))
    planet.screen.blit(txt, (20, 70))

    pygame.display.update()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    text = pygame.font.Font(None, 24)
    finished = False

    rocket = Rocket(screen)
    planet = Planet(screen)

    while not finished:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                planet.move_screen("down", event)
            elif event.type == pygame.MOUSEMOTION:
                planet.move_screen("motion", event)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                planet.move_screen("up", event)

        pygame.display.update()

        rocket.turn(pygame.key.get_pressed())
        rocket.switch_engine(pygame.key.get_pressed())

        calculate_rocket(rocket, planet)

        screen.fill(COSMIC)
        planet.change_mode(pygame.key.get_pressed())
        planet.change_mode_timer_count()

        planet.draw(rocket)
        rocket.draw(planet)
        rocket.draw_fuel_tank()
        planet.time_scale(pygame.key.get_pressed())
        planet.time_scale_counter_timer()
        planet.time_scale_to_rocket_counter_timer()
        planet.scale(pygame.key.get_pressed(), rocket)

        text_score(text, planet, rocket)
        calculate_physical_time(planet)

    pygame.quit()


if __name__ == "__main__":
    main()