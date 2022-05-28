from config import BOARD_POINT, CELL_W, COLS, ROWS
import main
from game_character import GameCharacter
YELLOW = (255, 255, 0)


class PacMan(GameCharacter):
    game: main.Game

    def __init__(self, game: main.Game,  x: int, y: int, dir: tuple):
        super().__init__(game, x, y, YELLOW, dir)
        self.pace = 1/120

    def collect_points(self):
        if self.in_cell_center():
            i = (int(self.pos.x) // CELL_W) % COLS
            j = (int(self.pos.y) // CELL_W) % ROWS

            if self.game.board[j][i] == BOARD_POINT:
                self.game.board[j][i] = 0
                self.game.incr_point_count(20)

    def update_state(self):
        super().update_state()
        self.collect_points()
