from model import *
from classes import *

FPS = 60


def text_score(text, planet, rocket):
    txt = text.render('time: ' + f"{planet.time:.{1}f}" + " s", True, (139, 0, 255))
    planet.screen.blit(txt, (20, 30))
    txt = text.render('height: ' + f"{(rocket.x**2 + rocket.y**2)**0.5  - 6371_035:.{1}f}" + " м", True, (139, 0, 255))
    planet.screen.blit(txt, (20, 50))
    txt = text.render('time_scale: ' + f"{(planet.time_scale_array[planet.time_scale_index]):.{1}f}", True,
                      (139, 0, 255))
    planet.screen.blit(txt, (20, 70))
    txt = text.render('velocity: ' + f"{(rocket.vx**2 + rocket.vy**2)**0.5:.{1}f}", True,
                     (139, 0, 255))
    planet.screen.blit(txt, (20, 90))
    pygame.display.update()


def main():
    pygame.init()
    info_object = pygame.display.Info()
    width = info_object.current_w
    height = info_object.current_h
    screen = pygame.display.set_mode((1200, 900))
    clock = pygame.time.Clock()
    text = pygame.font.Font(None, 24)
    finished = False

    rocket = Rocket(screen, width, height)
    planet = Planet(screen, width, height)
    menu = Menu(screen, width, height)


    while not finished:

        clock.tick(FPS)
        for event in pygame.event.get():
            if menu.active:
                screen.fill(COSMIC)
                menu.draw()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
                    if (menu.play_button[0][0] < event.pos[0]) and (event.pos[0] < menu.play_button[3][0]) and \
                            (menu.play_button[0][1] < event.pos[1]) and (event.pos[1] < menu.play_button[3][1]):
                        rocket = menu.play

                    elif (menu.tutorial_button[0][0] < event.pos[0]) and (
                            event.pos[0] < menu.tutorial_button[3][0]) and \
                            (menu.tutorial_button[0][1] < event.pos[1]) and (
                            event.pos[1] < menu.tutorial_button[3][1]):
                        menu.tutorial()

                    elif (menu.authors_button[0][0] < event.pos[0]) and (
                            event.pos[0] < menu.authors_button[3][0]) and \
                            (menu.authors_button[0][1] < event.pos[1]) and (
                            event.pos[1] < menu.authors_button[3][1]):
                        menu.authors()

                    elif (menu.quit_button[0][0] < event.pos[0]) and (event.pos[0] < menu.quit_button[3, 0]) and \
                            (menu.quit_button[0][1] < event.pos[1]) and (event.pos[1] < menu.quit_button[3][1]):
                        finished = True

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





        if (not menu.active):
            rocket.turn(pygame.key.get_pressed())
            rocket.switch_engine(pygame.key.get_pressed())

            calculate_rocket(rocket, planet)

            screen.fill(COSMIC)
            planet.change_mode(pygame.key.get_pressed())
            planet.change_mode_timer_count()

            planet.draw(rocket)

            rocket.draw(planet)
            rocket.draw_fuel_tank()
            rocket.explosion(planet)
            planet.time_scale(pygame.key.get_pressed())
            planet.time_scale_counter_timer()
            planet.time_scale_to_rocket_counter_timer()
            planet.scale(pygame.key.get_pressed(), rocket)

            text_score(text, planet, rocket)
            calculate_physical_time(planet)


    pygame.quit()


if __name__ == "__main__":
    main()