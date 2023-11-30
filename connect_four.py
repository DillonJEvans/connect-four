from typing import List, Tuple, Optional

from player import Player

# Type aliases for convenience

Tile = Optional[Player]
Tiles = List[Tile]
TileGrid = List[Tiles]

Cell = Tuple[int, int]
Cells = Tuple[Cell]


class ConnectFour:
    """Handles game logic for Connect 4."""

    def __init__(self, rows: int = 6, columns: int = 7, connect_n: int = 4):
        """
        Creates a new game of Connect 4.

        :param rows: The number of rows.
        :param columns: The number of columns.
        :param connect_n: How many tiles in a row to win.
        """
        # Accessed like grid[row][column],
        # where grid[0][0] is the bottom-left of the grid,
        # and grid[0][columns] is the bottom-right of the grid.
        self.grid: TileGrid = [[]]
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
        cells = self.winning_cells()
        if cells is None:
            return None
        return self.grid[cells[0][0]][cells[0][1]]

    def winning_cells(self) -> Optional[Cells]:
        """
        Gets the locations in the grid where the winning tiles are.

        :return: Returns the cells that make up the winning connection,
                 or None of there is no winner.
        """
        def tile(connect_four: ConnectFour, cell: Tuple[int, int]) -> Tile:
            return connect_four.grid[cell[0]][cell[1]]

        for row in range(self.rows):
            for column in range(self.columns):
                player = self.grid[row][column]
                # Skip the cell if it is empty
                if player is None:
                    continue
                can_check_row = (column <= self.columns - self.connect_n)
                can_check_column = (row <= self.rows - self.connect_n)
                # Check row
                if can_check_row:
                    cells = tuple((row, column + i) for i in range(self.connect_n))
                    if all([tile(self, cell) == player for cell in cells]):
                        return cells
                # Check column
                if can_check_column:
                    cells = tuple((row + i, column) for i in range(self.connect_n))
                    if all([tile(self, cell) == player for cell in cells]):
                        return cells
                # Check diagonal
                if can_check_row and can_check_column:
                    cells = tuple((row + i, column + i) for i in range(self.connect_n))
                    if all([tile(self, cell) == player for cell in cells]):
                        return cells
        # No winner (either the game is not over, or it ended in a draw)
        return None

    def __str__(self) -> str:
        def player_to_str(player: Player):
            if player == Player.ONE:
                return 'O'
            elif player == Player.TWO:
                return 'X'
            return ' '

        column_numbers = '   ' + '   '.join(map(str, range(self.columns)))
        rows = [' | '.join(map(player_to_str, row)) for row in self.grid]
        rows = [f'{r:<2} {row}' for r, row in enumerate(rows)]
        rows.reverse()
        return '\n'.join(rows + [column_numbers])
