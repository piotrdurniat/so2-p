from math import ceil, floor
import pygame
import time

from config import CELL_W, COLS, HEIGHT, ROWS, SURFACE_COLOR, WIDTH
import main


class GameCharacter(pygame.sprite.Sprite):
    # time between movement of 1 pixel
    pace: float
    dir: pygame.Vector2
    start_pos: tuple
    pos: pygame.Vector2
    rect: pygame.rect.Rect

    next_dir: tuple

    def __init__(self, game: main.Game, x: int, y: int, color):
        super().__init__()
        self.game = game
        self.dir = pygame.Vector2()
        self.next_dir = (-1, -1)
        self.start_pos = (x * CELL_W, y * CELL_W)
        self.pos = pygame.Vector2()
        self.reset_pos()

        self.image = pygame.Surface([CELL_W, CELL_W])
        self.image.fill(SURFACE_COLOR)
        # self.image.set_colorkey(COLOR)

        pygame.draw.rect(self.image,
                         color,
                         pygame.rect.Rect(0, 0, CELL_W, CELL_W))

        self.rect = self.image.get_rect()
        self.update_img()

    def set_dir(self, dir: tuple):
        self.dir.x, self.dir.y = dir

    def turn(self, dir: tuple):
        self.next_dir = dir

    def update_img(self):
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def in_cell_center(self):
        return self.pos.x % CELL_W == 0 and self.pos.y % CELL_W == 0

    def cell_free(self, i: int, j: int) -> bool:
        if i >= 0 and i <= COLS and j >= 0 and j <= ROWS:
            return self.game.board[j][i] != 1

        return True

    def move(self):

        if self.next_dir != (-1, -1):

            if self.dir.x == -self.next_dir[0] and self.dir.y == -self.next_dir[1]:
                self.dir.x, self.dir.y = self.next_dir
                self.next_dir = (-1, -1)

            elif self.in_cell_center():
                self.dir.x, self.dir.y = self.next_dir
                self.next_dir = (-1, -1)

        self.pos.x += self.dir.x
        self.pos.y += self.dir.y

        if self.pos.x > WIDTH:
            self.pos.x -= WIDTH
        elif self.pos.x < 0:
            self.pos.x += WIDTH

        if self.pos.y > HEIGHT:
            self.pos.y -= HEIGHT
        elif self.pos.y < 0:
            self.pos.y += HEIGHT

    def update_state(self):
        self.move()
        self.update_img()

    def reset_pos(self):
        self.pos.x, self.pos.y = self.start_pos

    def run(self):
        while True:
            if self.game.paused == False:
                time.sleep(self.pace)
                self.update_state()
