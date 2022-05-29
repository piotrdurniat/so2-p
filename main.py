#!/usr/bin/env python3
import threading
from typing import List
import pygame
import time

import config
import ghost
import pac_man
import hud


class Game:
    _life_lock: threading.Lock
    _point_lock: threading.Lock
    life_count: int
    point_count: int
    paused: bool
    board: List[List[int]]
    sprites: list
    sprite_group: pygame.sprite.Group

    def __init__(self):
        self._life_lock = threading.Lock()
        self._point_lock = threading.Lock()
        self.life_count = 3
        self.point_count = 0
        self.paused = False
        self.init_board()
        self.sprites = list()
        self.sprite_group = pygame.sprite.Group()

        pygame.init()
        pygame.display.set_caption("Pac-Man")
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        self.hud = hud.Hud(self.screen)

        ghost_red_img, ghost_cyan_img, ghost_magenta_img, ghost_orange_img, pac_man_images =\
            self.load_images()

        self.the_pac_man = pac_man.PacMan(
            self, 9, 16, config.DIR["LEFT"], pac_man_images
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

        self.sprites.extend([
            self.the_pac_man,
            ghost_red,
            ghost_cyan,
            ghost_magenta,
            ghost_orange
        ])

        for sprite in self.sprites:
            self.sprite_group.add(sprite)

        # Staring threads for sprites:
        for sprite in self.sprites:
            threading.Thread(target=sprite.run, daemon=True).start()

    def start(self):
        self.pause()
        self.draw_frame()
        time.sleep(3)
        self.resume()

        clock = pygame.time.Clock()
        game_on = True
        while game_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_on = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        game_on = False

            self.get_keys()
            self.draw_frame()
            clock.tick(60)

        pygame.quit()

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.the_pac_man.turn(config.DIR["LEFT"])
        if keys[pygame.K_RIGHT]:
            self.the_pac_man.turn(config.DIR["RIGHT"])
        if keys[pygame.K_DOWN]:
            self.the_pac_man.turn(config.DIR["DOWN"])
        if keys[pygame.K_UP]:
            self.the_pac_man.turn(config.DIR["UP"])

    def draw_frame(self):

        # Draw board
        self.screen.fill(config.SURFACE_COLOR)
        self.draw_board(self.screen)

        # Draw sprites
        self.sprite_group.draw(self.screen)

        # Draw HUD
        if self.paused:
            if self.life_count > 0:
                self.hud.center_text("Get ready")
            else:
                self.hud.center_text("Game over")

        self.hud.show_point_count(self.point_count)
        self.hud.show_live_count(self.life_count)

        pygame.display.flip()

    def load_images(self) -> tuple:
        ghost_red = pygame.image.load('assets/ghost-red.png')
        ghost_cyan = pygame.image.load('assets/ghost-cyan.png')
        ghost_magenta = pygame.image.load('assets/ghost-magenta.png')
        ghost_orange = pygame.image.load('assets/ghost-orange.png')
        pac_man_img_1 = pygame.image.load('assets/pac-man-1.png')
        pac_man_img_2 = pygame.image.load('assets/pac-man-2.png')
        pac_man_img_3 = pygame.image.load('assets/pac-man-3.png')

        return (ghost_red, ghost_cyan, ghost_magenta, ghost_orange, [pac_man_img_1, pac_man_img_2, pac_man_img_3])

    def decr_live_count(self):
        with self._life_lock:
            self.life_count -= 1

            if self.life_count <= 0:
                self.end_game()
                return

            self.pause()
            time.sleep(1)
            for sprite in self.sprites:
                sprite.reset_pos()
            time.sleep(1)
            self.resume()

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
        for sprite in self.sprites:
            sprite.pause()

    def resume(self):
        self.paused = False
        for sprite in self.sprites:
            sprite.resume()

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

        for i in range(config.COLS):
            for j in range(config.ROWS):
                x = i * config.CELL_W
                y = j * config.CELL_W

                if self.board[j][i] == config.BOARD_WALL:
                    pygame.draw.rect(
                        surface,
                        WALL_COLOR,
                        pygame.Rect(x, y, config.CELL_W, config.CELL_W)
                    )
                if self.board[j][i] == config.BOARD_POINT:
                    pygame.draw.circle(
                        surface,
                        POINT_COLOR,
                        (x + config.CELL_W // 2, y + config.CELL_W // 2),
                        config.CELL_W // 6
                    )


if __name__ == "__main__":
    game = Game()
    game.start()
