#!/usr/bin/env python3
import threading
import pygame
import time

from config import BOARD_POINT, BOARD_WALL, CELL_W, COLS, HEIGHT, ROWS, WIDTH, SURFACE_COLOR, DIR
import ghost
import pac_man
import hud


class Game:
    _live_lock: threading.Lock
    _point_lock: threading.Lock
    live_count: int
    point_count: int
    paused: bool
    board: list
    ghosts: list

    def __init__(self):
        self._live_lock = threading.Lock()
        self._point_lock = threading.Lock()
        self.live_count = 3
        self.point_count = 100
        self.paused = False
        self.init_board()

        pygame.init()
        size = (WIDTH, HEIGHT)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Pac-Man")

        all_sprites_list = pygame.sprite.Group()

        ghost_red_img, ghost_cyan_img, ghost_magenta_img, ghost_orange_img = self.load_images()

        self.the_pac_man = pac_man.PacMan(
            self, 9, 16, DIR["LEFT"], ghost_magenta_img
        )
        ghost_red = ghost.Ghost(
            self, 9, 10, self.the_pac_man, ghost_red_img
        )
        ghost_cyan = ghost.Ghost(
            self, 10, 10, self.the_pac_man, ghost_cyan_img
        )
        ghost_magenta = ghost.Ghost(
            self, 10, 10, self.the_pac_man, ghost_magenta_img
        )
        ghost_orange = ghost.Ghost(
            self, 10, 10, self.the_pac_man, ghost_orange_img
        )

        self.ghosts = [ghost_red, ghost_cyan, ghost_magenta, ghost_orange]
        self.hud = hud.Hud(screen)

        all_sprites_list.add(self.the_pac_man)
        for ghost_sprite in self.ghosts:
            all_sprites_list.add(ghost_sprite)

        # Staring threads for sprites:
        threading.Thread(target=self.the_pac_man.run).start()
        for ghost_sprite in self.ghosts:
            threading.Thread(target=ghost_sprite.run).start()

        clock = pygame.time.Clock()

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
            self.draw_board(screen)
            all_sprites_list.draw(screen)

            if self.paused:
                if self.live_count > 0:
                    self.hud.center_text("Get ready")
                else:
                    self.hud.center_text("Game over")

            self.hud.show_point_count(self.point_count)
            self.hud.show_live_count(self.live_count)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def load_images(self) -> tuple:
        ghost_red = pygame.image.load('assets/ghost-red.png')
        ghost_cyan = pygame.image.load('assets/ghost-cyan.png')
        ghost_magenta = pygame.image.load('assets/ghost-magenta.png')
        ghost_orange = pygame.image.load('assets/ghost-orange.png')

        return (ghost_red, ghost_cyan, ghost_magenta, ghost_orange)

    def decr_live_count(self):
        with self._live_lock:
            self.pause()
            self.live_count -= 1
            self.decr_point_count(10)

            if self.live_count <= 0:
                self.end_game()
                return

            time.sleep(2)
            self.resume()
            self.the_pac_man.reset_pos()

            for ghost in self.ghosts:
                ghost.reset_pos()

    def decr_point_count(self, points):
        with self._point_lock:
            self.point_count -= points

    def incr_point_count(self, points):
        with self._point_lock:
            self.point_count += points

    def end_game(self):
        self.pause()
        self.hud.center_text("Game over")

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def init_board(self):
        self.board = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1],
            [0, 0, 0, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 0, 0],
            [1, 1, 1, 1, 2, 1, 2, 1, 1, 0, 1, 1, 2, 1, 2, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1],
            [0, 0, 0, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 0, 0],
            [1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
            [1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1],
            [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
            [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def draw_board(self, surface):
        WALL_COLOR = (0, 0, 150)
        POINT_COLOR = (200, 200, 200)

        for i in range(COLS):
            for j in range(ROWS):
                x = i * CELL_W
                y = j * CELL_W

                if self.board[j][i] == BOARD_WALL:
                    pygame.draw.rect(
                        surface,
                        WALL_COLOR,
                        pygame.Rect(x, y, CELL_W, CELL_W)
                    )
                if self.board[j][i] == BOARD_POINT:
                    pygame.draw.circle(
                        surface,
                        POINT_COLOR,
                        (x + CELL_W // 2, y + CELL_W // 2),
                        CELL_W // 6
                    )


if __name__ == "__main__":
    game = Game()
