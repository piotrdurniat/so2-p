import time
from config import BOARD_POINT, CELL_W, COLS, DIR, ROWS
import main
from game_character import GameCharacter
YELLOW = (255, 255, 0)


class PacMan(GameCharacter):
    game: main.Game

    def __init__(self, game: main.Game,  x: int, y: int):
        super().__init__(game, x, y, YELLOW)
        self.pace = 1/120
        self.set_dir(DIR["UP"])

    def collect_points(self):
        i = self.pos.x / CELL_W
        j = self.pos.y / CELL_W

        if i.is_integer() and j.is_integer():

            i = int(i)
            j = int(j)

            if i >= 0 and i < COLS and j >= 0 and j < ROWS and self.game.board[j][i] == BOARD_POINT:
                self.game.board[j][i] = 0
                self.game.incr_point_count(20)

    def update_state(self):
        super().update_state()
        self.collect_points()
