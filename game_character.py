from math import ceil, floor
import pygame
import time

from config import CELL_W, COLS, HEIGHT, ROWS, SURFACE_COLOR, WIDTH
import main


class GameCharacter(pygame.sprite.Sprite):
    # time between movement of 1 pixel
    pace: float

    dir: pygame.Vector2
    next_dir: pygame.Vector2
    start_pos: tuple
    pos: pygame.Vector2
    rect: pygame.rect.Rect

    def __init__(self, game: main.Game, x: int, y: int, color, dir: tuple):
        super().__init__()
        self.game = game
        self.dir = pygame.Vector2(dir[0], dir[1])
        self.next_dir = pygame.Vector2(dir[0], dir[1])
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

    def turn(self, dir: tuple):
        self.next_dir.update(dir[0], dir[1])

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

        # if next_dir is not the same as current dir
        if self.next_dir.x != self.dir.x or self.next_dir.y != self.dir.y:

           # Turing back happens immediately
            if self.dir.x == -self.next_dir.x and self.dir.y == -self.next_dir.y:
                self.dir.update(self.next_dir.x, self.next_dir.y)
                self.next_dir.update(self.dir.x, self.dir.y)

            # Turing to either side can only occur in the cell center
            elif self.in_cell_center():

                self.dir.update(self.next_dir.x, self.next_dir.y)
                self.next_dir.update(self.dir.x, self.dir.y)

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
