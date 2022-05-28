import random
from config import CELL_W, DIR
from pac_man import PacMan
from numpy import sign

from game_character import GameCharacter
import main

COLOR = (200, 0, 200)


class Ghost(GameCharacter):
    pac_man: PacMan

    def __init__(self, game: main.Game, x: int, y: int, pac_man: PacMan):
        dir = self.get_random_dir()
        super().__init__(game, x, y, COLOR, dir)
        self.pac_man = pac_man
        self.pace = 1/80

    def eat_pac_man(self):
        dist = self.pos.distance_to(self.pac_man.pos)
        if dist < CELL_W:
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
        return random.choice(list(DIR.values()))

    def random_turn(self):
        if (random.random() < 0.01):
            new_dir = self.get_random_dir()
            self.turn(new_dir)

    def update_state(self):
        self.random_turn()
        self.follow_pac_man()
        self.eat_pac_man()
        super().update_state()
