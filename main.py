from model import *
from classes import *
from interface import *

FPS = 60


def main():
    """
    Главная функция главного модуля.
    Создаёт окно, объекты и главный цикл игры
    """

    # создаём окно с размером пользовательского экран
    pygame.init()
    info_object = pygame.display.Info()
    width = info_object.current_w
    height = info_object.current_h
    screen = pygame.display.set_mode((width, height))

    # настройка pygame
    clock = pygame.time.Clock()
    text = pygame.font.Font(None, 24)
    finished = False

    # создаём объекты: ракету и Землю
    rocket = Rocket(screen, width, height)
    planet = Planet(screen, width, height)

    while not finished:

        clock.tick(FPS)
        # обрабатываем
        for event in pygame.event.get():
            # выход из игры
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    finished = True
            # обработка событий мыши для передвижения в режиме карты
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                planet.move_screen("down", event)
            elif event.type == pygame.MOUSEMOTION:
                planet.move_screen("motion", event)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                planet.move_screen("up", event)

        pygame.display.update()
        # управление ракетой
        rocket.turn(pygame.key.get_pressed())
        rocket.switch_engine(pygame.key.get_pressed())

        # расчёт физики, использует функции в model.py
        calculate_physics(rocket, planet)

        # управление параметрами отображения
        planet.change_mode(pygame.key.get_pressed())
        planet.time_scale(pygame.key.get_pressed())
        planet.time_scale_counter_timer()
        planet.time_scale_to_rocket_counter_timer()
        planet.scale(pygame.key.get_pressed(), rocket)
        planet.change_mode(pygame.key.get_pressed())
        planet.change_mode_timer_count()

        # отрисовка элементов игры
        screen.fill(COSMIC)
        planet.draw(rocket)
        rocket.draw(planet)
        rocket.draw_fuel_tank()
        rocket.explosion(planet)

        # отображение информации о ракете
        text_score(text, planet, rocket)

    pygame.quit()


if __name__ == "__main__":
    main()
