#!/usr/bin/env python3
import threading
import pygame

from config import HEIGHT, WIDTH, SURFACE_COLOR, DIR
from ghost import Ghost
from pac_man import PacMan

if __name__ == "__main__":

    pygame.init()

    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pac-Man")

    all_sprites_list = pygame.sprite.Group()

    pac_man = PacMan(200, 200, 20, 20)
    ghost = Ghost(10, 10, 20, 20, pac_man)
    ghost2 = Ghost(100, 100, 20, 20, pac_man)

    all_sprites_list.add(pac_man)
    all_sprites_list.add(ghost)
    all_sprites_list.add(ghost2)

    clock = pygame.time.Clock()

    pac_man_thread = threading.Thread(target=pac_man.run)
    ghost_thread = threading.Thread(target=ghost.run)
    ghost2_thread = threading.Thread(target=ghost2.run)

    pac_man_thread.start()
    ghost_thread.start()
    ghost2_thread.start()

    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game_on = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pac_man.set_dir(DIR["LEFT"])
        if keys[pygame.K_RIGHT]:
            pac_man.set_dir(DIR["RIGHT"])
        if keys[pygame.K_DOWN]:
            pac_man.set_dir(DIR["DOWN"])
        if keys[pygame.K_UP]:
            pac_man.set_dir(DIR["UP"])

        all_sprites_list.update()
        screen.fill(SURFACE_COLOR)
        all_sprites_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
