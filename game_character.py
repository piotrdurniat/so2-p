import pygame

from config import HEIGHT, SURFACE_COLOR, WIDTH


class GameCharacter(pygame.sprite.Sprite):

    # time between movement of 1 pixel
    pace: float
    dir: pygame.Vector2
    pos: pygame.Vector2
    rect: pygame.rect.Rect

    def __init__(self, x: int, y: int, width: int, height: int, color):
        super().__init__()

        self.dir = pygame.Vector2(0, 1)
        self.pos = pygame.Vector2(x, y)

        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        # self.image.set_colorkey(COLOR)

        pygame.draw.rect(self.image,
                         color,
                         pygame.rect.Rect(0, 0, width, height))

        self.rect = self.image.get_rect()
        self.update_img()

    def set_dir(self, dir: tuple):
        (self.dir.x, self.dir.y) = dir

    def update_img(self):
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def move(self):
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
