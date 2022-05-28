import pygame
import time
import threading

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
    _live_lock: threading.Lock

    def __init__(self, game: main.Game, x: int, y: int, color, dir: tuple):
        super().__init__()
        self._turn_lock = threading.Lock()

        self.game = game
        self.dir = pygame.Vector2(dir[0], dir[1])
        self.next_dir = pygame.Vector2(dir[0], dir[1])
        self.start_pos = (x * CELL_W, y * CELL_W)
        self.pos = pygame.Vector2()
        self.reset_pos()

        self.image = pygame.Surface([CELL_W, CELL_W])
        self.image.fill(SURFACE_COLOR)
        # self.image.set_colorkey(COLOR)

        pygame.draw.rect(
            self.image,
            color,
            pygame.rect.Rect(0, 0, CELL_W, CELL_W)
        )

        self.rect = self.image.get_rect()
        self.update_img()

    def turn(self, dir: tuple):
        with self._turn_lock:
            self.next_dir.update(dir[0], dir[1])

    def update_img(self):
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def in_cell_center(self):
        return self.pos.x % CELL_W == 0 and self.pos.y % CELL_W == 0

    def cell_free(self, i: int, j: int) -> bool:
        if i >= 0 and i < COLS and j >= 0 and j < ROWS:
            return self.game.board[j][i] != 1
        return True

    def next_cell_free(self):
        x = int(self.pos.x) // CELL_W + int(self.next_dir.x)
        y = int(self.pos.y) // CELL_W + int(self.next_dir.y)
        return self.cell_free(x, y)

    def opposite_vectors(self, vec1: pygame.Vector2, vec2: pygame.Vector2):
        return vec1.x == -vec2.x and vec1.y == -vec2.y

    def equal_vec(self, vec1, vec2):
        return vec1.x == vec2.x and vec1.y == vec2.y

    def move(self):
        with self._turn_lock:
            # Turing back happens immediately
            if self.opposite_vectors(self.dir, self.next_dir):
                self.dir.update(self.next_dir.x, self.next_dir.y)
                self.next_dir.update(self.dir.x, self.dir.y)

            # Turing can only occur in the cell center
            elif self.in_cell_center():
                if self.next_cell_free():
                    self.dir.update(self.next_dir.x, self.next_dir.y)
                    self.next_dir.update(self.dir.x, self.dir.y)

                # reset next_dir if turning not posible
                else:
                    self.next_dir.update(self.dir.x, self.dir.y)
                    # if going forward after reset still not posibble then stop
                    if not self.next_cell_free():
                        self.dir.update(0, 0)
                        self.next_dir.update(0, 0)

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
