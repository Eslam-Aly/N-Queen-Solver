import random
from typing import List, Tuple

class NQueenBoard:
    def __init__(self, n: int, seed: int = None):
        """
        Initializes an N x N board with one queen per row, placed randomly in a column.
        An optional seed ensures the initial state is consistent across algorithms.
        """
        self.n = n
        self.board = [[0] * n for _ in range(n)]
        self.queen_positions: List[Tuple[int, int]] = []

        if seed is not None:
            random.seed(seed)

        self._generate_random_initial_state()

    def _generate_random_initial_state(self):
        """
        Randomly place one queen in each row (guarantees N queens total).
        """
        self.queen_positions.clear()
        for row in range(self.n):
            col = random.randint(0, self.n - 1)
            self.board[row][col] = 1
            self.queen_positions.append((row, col))

    def get_board(self) -> List[List[int]]:
        """
        Returns the full board matrix.
        """
        return self.board

    def print_board(self):
        """
        Prints the board to the console.
        """
        for row in self.board:
            print(" ".join("Q" if cell == 1 else "." for cell in row))
        print()

    def copy(self):
        """
        Returns a deep copy of this board.
        """
        new_board = NQueenBoard(self.n)
        new_board.board = [row[:] for row in self.board]
        new_board.queen_positions = self.queen_positions[:]
        return new_board

    def reset_board(self):
        """
        Clears the board and queen positions.
        """
        self.board = [[0] * self.n for _ in range(self.n)]
        self.queen_positions.clear()

    def calculate_conflicts(self) -> int:
        """
        Calculates the number of conflicting pairs of queens.
        """
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                r1, c1 = self.queen_positions[i]
                r2, c2 = self.queen_positions[j]
                if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    conflicts += 1
        return conflicts

    def __eq__(self, other) -> bool:
        return self.board == other.board

    def __hash__(self) -> int:
        return hash(tuple(tuple(row) for row in self.board))