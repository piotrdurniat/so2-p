from enum import Enum
import pygame
import time
import threading

# Global Variables
YELLOW = (255, 255, 0)
COLOR = (255, 100, 98)
SURFACE_COLOR = (0, 0, 0)
WIDTH = 400
HEIGHT = 400


class Vec2D:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.set(x, y)

    def set(self, x: int, y: int):
        self.x = x
        self.y = y


class PacMan(pygame.sprite.Sprite):

    # time between movement of 1 pixel
    pace: float
    dir: Vec2D
    pos: Vec2D

    def __init__(self, x: int, y: int, height: int, width: int):
        super().__init__()

        self.dir = Vec2D(0, 1)
        self.pos = Vec2D(x, y)
        self.pace = 1/100

        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)

        pygame.draw.rect(self.image,
                         YELLOW,
                         pygame.Rect(0, 0, width, height))

        self.rect = self.image.get_rect()
        self.update_img()

    def set_dir_up(self):
        self.dir.set(0, -1)

    def set_dir_down(self):
        self.dir.set(0, 1)

    def set_dir_right(self):
        self.dir.set(1, 0)

    def set_dir_left(self):
        self.dir.set(-1, 0)

    def update_img(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

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

    def run(self):
        while True:
            time.sleep(self.pace)
            self.move()
            self.update_img()


pygame.init()

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pac-Man")


all_sprites_list = pygame.sprite.Group()

pac_man = PacMan(200, 200, 20, 20)

all_sprites_list.add(pac_man)
clock = pygame.time.Clock()

thread = threading.Thread(target=pac_man.run)
thread.start()

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
        pac_man.set_dir_left()
    if keys[pygame.K_RIGHT]:
        pac_man.set_dir_right()
    if keys[pygame.K_DOWN]:
        pac_man.set_dir_down()
    if keys[pygame.K_UP]:
        pac_man.set_dir_up()

    all_sprites_list.update()
    screen.fill(SURFACE_COLOR)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
