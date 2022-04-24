import pygame

from config import CELL_W, HEIGHT, SURFACE_COLOR, WIDTH


class GameCharacter(pygame.sprite.Sprite):
    # time between movement of 1 pixel
    pace: float
    dir: pygame.Vector2
    pos: pygame.Vector2
    rect: pygame.rect.Rect
    next_dir: tuple

    def __init__(self, x: int, y: int, color):
        super().__init__()

        self.dir = pygame.Vector2(0, 1)
        self.next_dir = (0, 0)
        self.pos = pygame.Vector2(x * CELL_W, y * CELL_W)

        self.image = pygame.Surface([CELL_W, CELL_W])
        self.image.fill(SURFACE_COLOR)
        # self.image.set_colorkey(COLOR)

        pygame.draw.rect(self.image,
                         color,
                         pygame.rect.Rect(0, 0, CELL_W, CELL_W))

        self.rect = self.image.get_rect()
        self.update_img()

    def turn(self, dir: tuple):
        self.next_dir = dir

    def update_img(self):
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def in_cell_center(self):
        return self.pos.x % CELL_W == 0 and self.pos.y % CELL_W == 0

    def move(self):
        if self.in_cell_center() and self.next_dir != (0, 0):
            self.dir.x, self.dir.y = self.next_dir
            self.next_dir = (0, 0)

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
