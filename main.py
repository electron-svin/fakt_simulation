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
    menu = Menu(screen, width, height)

    while not finished:

        clock.tick(FPS)
        # обработка событий pygame
        for event in pygame.event.get():
            # игра в режиме меню
            if menu.active:
                screen.fill(COSMIC)
                menu.draw()
                if event.type == pygame.MOUSEBUTTONDOWN \
                        and (not menu.tutorial_button_active) \
                        and (not menu.authors_button_active):

                    if (menu.play_button[0][0] < event.pos[0]) and (event.pos[0] < menu.play_button[3][0]) and \
                            (menu.play_button[0][1] < event.pos[1]) and (event.pos[1] < menu.play_button[3][1]):
                        rocket = menu.play(width, height)
                        menu.active = False

                    elif (menu.tutorial_button[0][0] < event.pos[0]) and (
                            event.pos[0] < menu.tutorial_button[3][0]) and \
                            (menu.tutorial_button[0][1] < event.pos[1]) and (
                            event.pos[1] < menu.tutorial_button[3][1]):
                        menu.tutorial_button_active = True

                    elif (menu.authors_button[0][0] < event.pos[0]) and (
                            event.pos[0] < menu.authors_button[3][0]) and \
                            (menu.authors_button[0][1] < event.pos[1]) and (
                            event.pos[1] < menu.authors_button[3][1]):
                        menu.authors_button_active = True

                    elif (menu.quit_button[0][0] < event.pos[0]) and (event.pos[0] < menu.quit_button[3][0]) and \
                            (menu.quit_button[0][1] < event.pos[1]) and (event.pos[1] < menu.quit_button[3][1]):
                        finished = True

                if (event.type == pygame.KEYDOWN) and (event.key == 27):
                    menu.authors_button_active = False
                    menu.tutorial_button_active = False
                menu.tutorial()
                menu.authors()
            # взаимодействие с мышью в режиме карты
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    menu.active = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                planet.move_screen("down", event)
            elif event.type == pygame.MOUSEMOTION:
                planet.move_screen("motion", event)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                planet.move_screen("up", event)

        pygame.display.update()
        # игра в режиме симуляции полёта
        if not menu.active:
            rocket.turn(pygame.key.get_pressed())
            rocket.switch_engine(pygame.key.get_pressed())

            # обработка физики
            calculate_physics(rocket, planet)
            calculate_physical_time(planet)

            # отрисовка элементов игры
            screen.fill(COSMIC)
            planet.draw(rocket)
            rocket.draw(planet)
            rocket.draw_fuel_tank()
            rocket.explosion(planet)
            text_score(text, planet, rocket)

            # обработка нажатий клавиш
            planet.time_scale(pygame.key.get_pressed())
            planet.scale(pygame.key.get_pressed(), rocket)
            planet.change_mode(pygame.key.get_pressed())

            # таймеры
            planet.time_scale_counter_timer()
            planet.time_scale_to_rocket_counter_timer()
            planet.change_mode_timer_count()

    pygame.quit()


if __name__ == "__main__":
    main()
