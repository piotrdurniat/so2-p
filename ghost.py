import random
import time
from math import copysign

from game_character import GameCharacter
from pac_man import PacMan
from config import DIR

BLUE = (0, 0, 255)


class Ghost(GameCharacter):
    pac_man: PacMan

    def __init__(self, x: int, y: int, pac_man: PacMan):
        super().__init__(x, y, BLUE)
        self.pac_man = pac_man
        self.pace = 1/80

    def follow_pac_man(self):
        dist = self.pos.distance_to(self.pac_man.pos)

        if dist < 100:
            x_diff = self.pac_man.pos.x - self.pos.x
            y_diff = self.pac_man.pos.y - self.pos.y

            if abs(x_diff) > abs(y_diff):
                new_dir = (copysign(1, x_diff), 0)
                self.turn(new_dir)
            else:
                new_dir = (0, copysign(1, y_diff))
                self.turn(new_dir)

    def random_turn(self):
        if (random.random() < 0.01):
            new_dir = random.choice(list(DIR.values()))
            self.turn(new_dir)

    def run(self):
        while True:
            time.sleep(self.pace)
            self.random_turn()
            self.follow_pac_man()
            self.move()
            self.update_img()
