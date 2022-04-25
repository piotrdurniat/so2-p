#!/usr/bin/env python3
import threading
import pygame
import time

from config import CELL_W, COLS, HEIGHT, ROWS, WIDTH, SURFACE_COLOR, DIR
import ghost
import pac_man


class Game:
    _live_lock: threading.Lock
    _point_lock: threading.Lock
    live_count: int
    point_count: int
    paused: bool

    def decr_live_count(self):
        with self._live_lock:
            self.pause()
            self.live_count -= 1
            print("live_count: ", self.live_count)
            self.decr_point_count(10)

            if self.live_count == 0:
                self.end_game()
                return

            time.sleep(2)
            self.resume()
            self.the_pac_man.reset_pos()
            self.ghost1.reset_pos()
            self.ghost2.reset_pos()

    def decr_point_count(self, points):
        with self._point_lock:
            self.point_count -= points
            print("point_count: ", self.point_count)

    def incr_point_count(self, points):
        with self._point_lock:
            self.point_count += points
            print("point_count: ", self.point_count)

    def end_game(self):
        self.paused = True
        print("Game over")

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def __init__(self):
        self._live_lock = threading.Lock()
        self._point_lock = threading.Lock()
        self.live_count = 3
        self.point_count = 100
        self.paused = False

        pygame.init()
        size = (WIDTH, HEIGHT)
        screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Pac-Man")

        all_sprites_list = pygame.sprite.Group()

        self.the_pac_man = pac_man.PacMan(self, 6, 16)
        self.ghost1 = ghost.Ghost(self, 6, 7, self.the_pac_man)
        self.ghost2 = ghost.Ghost(self, 8, 7, self.the_pac_man)

        all_sprites_list.add(self.the_pac_man)
        all_sprites_list.add(self.ghost1)
        all_sprites_list.add(self.ghost2)

        clock = pygame.time.Clock()

        pac_man_thread = threading.Thread(target=self.the_pac_man.run)
        ghost_thread = threading.Thread(target=self.ghost1.run)
        ghost2_thread = threading.Thread(target=self.ghost2.run)

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
                self.the_pac_man.turn(DIR["LEFT"])
            if keys[pygame.K_RIGHT]:
                self.the_pac_man.turn(DIR["RIGHT"])
            if keys[pygame.K_DOWN]:
                self.the_pac_man.turn(DIR["DOWN"])
            if keys[pygame.K_UP]:
                self.the_pac_man.turn(DIR["UP"])

            all_sprites_list.update()
            screen.fill(SURFACE_COLOR)
            draw_grid(screen)
            all_sprites_list.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


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
    game = Game()
