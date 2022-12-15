import pygame


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