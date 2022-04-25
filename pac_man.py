import time
from config import DIR
import main
from game_character import GameCharacter
YELLOW = (255, 255, 0)


class PacMan(GameCharacter):
    game: main.Game

    def __init__(self, game: main.Game,  x: int, y: int):
        super().__init__(game, x, y, YELLOW)
        self.pace = 1/120
        self.set_dir(DIR["UP"])

    def update_state(self):
        super().update_state()
