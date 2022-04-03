import pygame
# from pygame import Vector2
# from pygame.sprite import Sprite
# from pygame.rect import Rect
# from pygame import Surface
import time
import threading

# Global Variables
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
SURFACE_COLOR = (0, 0, 0)
WIDTH = 400
HEIGHT = 400


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
        self.pace = 1/100

        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        # self.image.set_colorkey(COLOR)

        pygame.draw.rect(self.image,
                         color,
                         pygame.rect.Rect(0, 0, width, height))

        self.rect = self.image.get_rect()
        self.update_img()

    def set_dir_up(self):
        self.dir.x = 0
        self.dir.y = -1

    def set_dir_down(self):
        self.dir.x = 0
        self.dir.y = 1

    def set_dir_right(self):
        self.dir.x = 1
        self.dir.y = 0

    def set_dir_left(self):
        self.dir.x = -1
        self.dir.y = 0

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


class PacMan(GameCharacter):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, YELLOW)

    def run(self):
        while True:
            time.sleep(self.pace)
            self.move()
            self.update_img()


class Ghost(GameCharacter):
    pac_man: PacMan

    def __init__(self, x: int, y: int, width: int, height: int, pac_man: PacMan):
        super().__init__(x, y, width, height, BLUE)
        self.pac_man = pac_man

    def follow_pac_man(self):
        dist = self.pos.distance_to(self.pac_man.pos)

        if dist < 200:
            pass

    def run(self):
        while True:
            time.sleep(self.pace)

            self.follow_pac_man()
            self.move()
            self.update_img()


pygame.init()

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pac-Man")


all_sprites_list = pygame.sprite.Group()

pac_man = PacMan(200, 200, 20, 20)
ghost = Ghost(10, 10, 20, 20, pac_man)

all_sprites_list.add(pac_man)
all_sprites_list.add(ghost)

clock = pygame.time.Clock()

pac_man_thread = threading.Thread(target=pac_man.run)
ghost_thread = threading.Thread(target=ghost.run)
pac_man_thread.start()
ghost_thread.start()

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
