from typing import List
import pygame

import config
import main
from game_character import GameCharacter


class PacMan(GameCharacter):
    game: main.Game
    img_index = 0
    frame_count = 0
    images: List[pygame.surface.Surface]

    def __init__(self, game: main.Game,  x: int, y: int, dir: tuple, images: List[pygame.surface.Surface]):
        super().__init__(game, x, y, dir, images[0])
        self.pace = 1/120
        self.images = list()
        for img in images:
            self.images.append(pygame.transform.scale(
                img, (config.CELL_W, config.CELL_W)
            ))

    def collect_points(self):
        if self.in_cell_center():
            i = (int(self.pos.x) // config.CELL_W) % config.COLS
            j = (int(self.pos.y) // config.CELL_W) % config.ROWS

            if self.game.board[j][i] == config.BOARD_POINT:
                self.game.board[j][i] = 0
                self.game.incr_point_count(1)

    def update_animation(self):
        self.img_index += 1
        self.img_index %= 3
        self.image = self.images[self.img_index]

        angle = 0
        if self.dir == config.DIR["UP"]:
            angle = 270
        if self.dir == config.DIR["RIGHT"]:
            angle = 180
        if self.dir == config.DIR["DOWN"]:
            angle = 90

        self.image = pygame.transform.rotate(self.image, angle)

    def update_state(self):
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.update_animation()

        super().update_state()
        self.collect_points()
