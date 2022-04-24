import random
import time
from math import copysign

from game_character import GameCharacter
from pac_man import PacMan
from config import DIR

BLUE = (0, 0, 255)


class Ghost(GameCharacter):
    pac_man: PacMan

    def __init__(self, x: int, y: int, width: int, height: int, pac_man: PacMan):
        super().__init__(x, y, width, height, BLUE)
        self.pac_man = pac_man
        self.pace = 1/80

    def follow_pac_man(self):
        dist = self.pos.distance_to(self.pac_man.pos)

        if dist < 100:
            x_diff = self.pac_man.pos.x - self.pos.x
            y_diff = self.pac_man.pos.y - self.pos.y

            if abs(x_diff) > abs(y_diff):
                self.dir.x = copysign(1, x_diff)
                self.dir.y = 0
            else:
                self.dir.y = copysign(1, y_diff)
                self.dir.x = 0

    def random_turn(self):
        if (random.random() < 0.01):
            new_dir = random.choice(list(DIR.values()))
            print(new_dir)
            self.set_dir(new_dir)

    def run(self):
        while True:
            time.sleep(self.pace)
            self.random_turn()
            self.follow_pac_man()
            self.move()
            self.update_img()
