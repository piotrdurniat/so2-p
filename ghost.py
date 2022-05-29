import random
import pygame
from numpy import sign

from pac_man import PacMan
import config
from game_character import GameCharacter
import main


class Ghost(GameCharacter):
    pac_man: PacMan

    def __init__(self, game: main.Game, x: int, y: int, pac_man: PacMan, img: pygame.surface.Surface):
        dir = self.get_random_dir()
        super().__init__(game, x, y, dir, img)
        self.pac_man = pac_man
        self.pace = 1/80
        self.img = img

    def eat_pac_man(self):
        dist = self.pos.distance_to(self.pac_man.pos)
        if dist < config.CELL_W and not self.paused:
            self.game.decr_live_count()

    def follow_pac_man(self):
        dist = self.pos.distance_to(self.pac_man.pos)

        if dist < 100:
            x_diff = self.pac_man.pos.x - self.pos.x
            y_diff = self.pac_man.pos.y - self.pos.y

            if abs(x_diff) > abs(y_diff):
                new_dir = (sign(x_diff), 0)
                self.turn(new_dir)
            else:
                new_dir = (0, sign(y_diff))
                self.turn(new_dir)

    def get_random_dir(self):
        return random.choice(list(config.DIR.values()))

    def random_turn(self):
        if (self.dir.x == 0 and self.dir.y == 0) or (random.random() < 0.016):
            new_dir = self.get_random_dir()
            self.turn(new_dir)

    def update_state(self):
        self.random_turn()
        self.follow_pac_man()
        self.eat_pac_man()
        super().update_state()
