import time

from game_character import GameCharacter

YELLOW = (255, 255, 0)


class PacMan(GameCharacter):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, YELLOW)
        self.pace = 1/120

    def run(self):
        while True:
            time.sleep(self.pace)
            self.move()
            self.update_img()
