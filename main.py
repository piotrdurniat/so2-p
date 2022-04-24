#!/usr/bin/env python3
import threading
import pygame

from config import CELL_W, COLS, HEIGHT, ROWS, WIDTH, SURFACE_COLOR, DIR
from ghost import Ghost
from pac_man import PacMan


def draw_grid(surface):
    color = (100, 100, 100)
    for i in range(COLS):
        for j in range(ROWS):
            x = i * CELL_W
            y = j * CELL_W
            pygame.draw.rect(surface,
                             color,
                             pygame.Rect(x, y, CELL_W, CELL_W),
                             1)


if __name__ == "__main__":

    pygame.init()

    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Pac-Man")

    all_sprites_list = pygame.sprite.Group()

    pac_man = PacMan(2, 3)
    ghost = Ghost(1, 5, pac_man)
    ghost2 = Ghost(4, 4, pac_man)

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
            pac_man.turn(DIR["LEFT"])
        if keys[pygame.K_RIGHT]:
            pac_man.turn(DIR["RIGHT"])
        if keys[pygame.K_DOWN]:
            pac_man.turn(DIR["DOWN"])
        if keys[pygame.K_UP]:
            pac_man.turn(DIR["UP"])

        all_sprites_list.update()
        screen.fill(SURFACE_COLOR)
        draw_grid(screen)
        all_sprites_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
