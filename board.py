import random
from typing import List, Tuple

class NQueenBoard:
    def __init__(self, n: int, seed: int = None):
        """
        Initializes an N x N chessboard for the N-Queens problem.
        Optionally accepts a seed for reproducible random initial states.
        """
        self.n = n
        self.board = [[0] * n for _ in range(n)]
        self.queen_positions: List[Tuple[int, int]] = []
        self.move_count = 0

        if seed is not None:
            random.seed(seed)
        self._generate_random_initial_state()

    def _generate_random_initial_state(self):
        """
        Randomly places one queen per row using a valid permutation.
        Ensures no column conflicts initially.
        """
        self.reset_board()
        cols = list(range(self.n))
        random.shuffle(cols)
        for row, col in enumerate(cols):
            self.place_queen(row, col)

    def place_queen(self, row: int, col: int):
        """
        Places a queen at (row, col).
        Removes any existing queen in that row first.
        """
        self.remove_queen(row)
        self.board[row][col] = 1
        self.queen_positions.append((row, col))
        self.move_count += 1

    def remove_queen(self, row: int):
        """
        Removes any queen in the given row.
        """
        for col in range(self.n):
            if self.board[row][col] == 1:
                self.board[row][col] = 0
                self.queen_positions.remove((row, col))
                return

    def calculate_conflicts(self) -> int:
        """
        Calculates number of conflicting queen pairs.
        """
        conflicts = 0
        for i in range(len(self.queen_positions)):
            for j in range(i + 1, len(self.queen_positions)):
                r1, c1 = self.queen_positions[i]
                r2, c2 = self.queen_positions[j]
                if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    conflicts += 1
        return conflicts

    def print_board(self):
        """
        Prints the current board to the console.
        """
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if self.board[row][col] == 1:
                    line += "Q "
                else:
                    line += ". "
            print(line.strip())
        print()

    def reset_board(self):
        """
        Clears the board and queen tracking.
        """
        self.board = [[0] * self.n for _ in range(self.n)]
        self.queen_positions.clear()
        self.move_count = 0

    def get_positions(self) -> List[Tuple[int, int]]:
        """
        Returns current queen positions.
        """
        return self.queen_positions

    def get_board_matrix(self) -> List[List[int]]:
        """
        Returns current board matrix.
        """
        return self.board

    def get_move_count(self) -> int:
        """
        Returns number of queen moves performed.
        """
        return self.move_count