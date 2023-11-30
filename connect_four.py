from typing import List, Optional

from player import Player


Cells = List[Optional[Player]]


class ConnectFour:
    """Handles game logic for Connect 4."""

    def __init__(self, rows: int = 6, columns: int = 7, connect_n: int = 4):
        """
        Creates a new game of Connect 4.

        :param rows: The number of rows.
        :param columns: The number of columns.
        :param connect_n: How many tiles in a row to win.
        """
        self.grid: List[Cells] = [[]]
        self.column_heights: List[int] = []
        self.rows: int = rows
        self.columns: int = columns
        self.connect_n: int = connect_n
        self.turn: Player = Player.ONE
        self.reset()

    def reset(self) -> None:
        """Resets the game."""
        self.grid = [[None] * self.columns for _ in range(self.rows)]
        self.column_heights = [0] * self.columns
        self.turn = Player.ONE

    def can_place(self, column: int) -> bool:
        """
        Checks if a tile can be placed in the specified column.
        AKA checks if the column is full.

        :param column: The column to check.
        :return: True if a tile can be placed in the column, false otherwise.
        """
        return self.column_heights[column] < self.rows

    def place(self, column: int) -> bool:
        """
        Places a tile for the current player in the specified column.
        Changes turn to the other player.

        :param column: The column to place the tile in.
        :return: True if placeable(column) is true, false otherwise.
        """
        if not self.can_place(column):
            return False
        row = self.column_heights[column]
        self.grid[row][column] = self.turn
        self.column_heights[column] += 1
        self.turn = Player(not self.turn)
        return True

    def is_over(self) -> bool:
        """
        Checks if the game is over or not.
        :return: True if the game is over, false otherwise.
        """
        is_winner = self.winner() is not None
        grid_is_full = not any(map(self.can_place, range(self.columns)))
        return is_winner or grid_is_full

    def winner(self) -> Optional[Player]:
        """
        Determines the winner of the game.

        You should use is_over() to check if the game has ended,
        and then winner() afterwards to determine the result.

        :return: The winner of the game,
                 or None if the game is either not over or ended in a draw.
        """

        # Helper functions that return N cells in the row/column/diagonal,
        # starting from grid[r][c].
        def row_cells(game: ConnectFour, r: int, c: int) -> Optional[Cells]:
            if c > game.columns - game.connect_n:
                return None
            return [game.grid[r][c + i] for i in range(game.connect_n)]

        def column_cells(game: ConnectFour, r: int, c: int) -> Optional[Cells]:
            if r > game.rows - game.connect_n:
                return None
            return [game.grid[r + i][c] for i in range(self.connect_n)]

        def diagonal_cells(game: ConnectFour, r: int, c: int) -> Optional[Cells]:
            if r > game.rows - game.connect_n:
                return None
            if c > game.columns - game.connect_n:
                return None
            return [game.grid[r + i][c + i] for i in range(self.connect_n)]

        for row in range(self.rows):
            for column in range(self.columns):
                player = self.grid[row][column]
                # Skip the cell if it is empty
                if player is None:
                    continue
                # Check row
                cells = row_cells(self, row, column)
                if cells is not None and all([cell == player for cell in cells]):
                    return player
                # Check column
                cells = column_cells(self, row, column)
                if cells is not None and all([cell == player for cell in cells]):
                    return player
                # Check diagonal
                cells = diagonal_cells(self, row, column)
                if cells is not None and all([cell == player for cell in cells]):
                    return player
        # No winner (either the game is not over, or it ended in a draw)
        return None

    def __str__(self) -> str:
        def player_to_str(player: Player):
            if player == Player.ONE:
                return 'O'
            elif player == Player.TWO:
                return 'X'
            return ' '
        rows = [' | '.join(map(player_to_str, row)) for row in self.grid]
        rows.reverse()
        return '\n'.join(rows)
