from player import Player


class ConnectFour:
    def __init__(self, rows: int = 6, columns: int = 7):
        self.grid = [[]]
        self.column_heights = []
        self.rows = rows
        self.columns = columns
        self.turn = Player.ONE
        self.reset()

    def reset(self) -> None:
        self.grid = [[None] * self.columns for row in range(self.rows)]
        self.column_heights = [0] * self.columns
        self.turn = Player.ONE

    def place(self, column: int) -> bool:
        row = self.column_heights[column]
        if row == self.rows:
            return False
        self.grid[row][column] = self.turn
        self.column_heights[column] += 1
        self.turn = Player(not self.turn)
        return True

    def __str__(self) -> str:
        def cell_to_str(cell: Player):
            if cell == Player.ONE:
                return 'O'
            elif cell == Player.TWO:
                return 'X'
            return ' '
        rows = [' | '.join([cell_to_str(cell) for cell in row]) for row in self.grid]
        rows = reversed(rows)
        return '\n'.join(rows)
