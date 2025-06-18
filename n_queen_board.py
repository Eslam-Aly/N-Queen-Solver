import random
from typing import List, Tuple

class NQueenBoard:
    def __init__(self, n: int, seed: int = None):
        """
        Initializes an N x N chessboard for the N-Queens problem.
        Optionally accepts a seed for reproducible random initial states.
        Also initializes internal structures for conflict tracking and move counting.
        """
        self.n = n
        self.board = [[0] * n for _ in range(n)]  # 2D board grid
        self.queen_positions: List[Tuple[int, int]] = []  # List of (row, col) positions of queens
        self.col_conflicts = [0] * n
        self.diag1_conflicts = [0] * (2 * n - 1)  # row - col + n - 1
        self.diag2_conflicts = [0] * (2 * n - 1)  # row + col
        self.move_count = 0  # Total number of queen moves (for benchmarking)

        if seed is not None:
            random.seed(seed)  # Ensures same initial state across algorithms

        self._generate_random_initial_state()

    def _generate_random_initial_state(self):
        """
        Randomly places one queen in each row.
        Ensures exactly N queens on the board, one per row.
        """
        self.reset_board()
        for row in range(self.n):
            col = random.randint(0, self.n - 1)
            self.place_queen(row, col)

    def place_queen(self, row: int, col: int):
        """
        Places a queen at (row, col), updating conflict counters.
        Removes any existing queen from that row first.
        """
        self.remove_queen(row)
        self.board[row][col] = 1
        self.queen_positions.append((row, col))
        self.col_conflicts[col] += 1
        self.diag1_conflicts[row - col + self.n - 1] += 1
        self.diag2_conflicts[row + col] += 1
        self.move_count += 1

    def remove_queen(self, row: int):
        """
        Removes any queen currently in the given row and updates conflict counters.
        """
        for col in range(self.n):
            if self.board[row][col] == 1:
                self.board[row][col] = 0
                self.queen_positions.remove((row, col))
                self.col_conflicts[col] -= 1
                self.diag1_conflicts[row - col + self.n - 1] -= 1
                self.diag2_conflicts[row + col] -= 1
                return

    def is_safe(self, row: int, col: int) -> bool:
        """
        Checks if placing a queen at (row, col) causes any conflicts.
        Returns True if the position is safe.
        """
        return (self.col_conflicts[col] == 0 and
                self.diag1_conflicts[row - col + self.n - 1] == 0 and
                self.diag2_conflicts[row + col] == 0)

    def calculate_conflicts(self) -> int:
        """
        Calculates the total number of conflicting queen pairs.
        Optimized using conflict counters.
        """
        conflicts = 0
        for row, col in self.queen_positions:
            conflicts += (self.col_conflicts[col] - 1)
            conflicts += (self.diag1_conflicts[row - col + self.n - 1] - 1)
            conflicts += (self.diag2_conflicts[row + col] - 1)
        return conflicts // 2  # Each conflict pair is counted twice

    def print_board(self):
        """
        Prints the board in human-readable format.
        """
        for row in self.board:
            print(" ".join("Q" if cell == 1 else "." for cell in row))
        print()

    def reset_board(self):
        """
        Resets the board and all tracking structures.
        Useful for rerunning algorithms or regenerating states.
        """
        self.board = [[0] * self.n for _ in range(self.n)]
        self.queen_positions.clear()
        self.col_conflicts = [0] * self.n
        self.diag1_conflicts = [0] * (2 * self.n - 1)
        self.diag2_conflicts = [0] * (2 * self.n - 1)
        self.move_count = 0

    def get_board(self) -> List[List[int]]:
        """
        Returns the current board matrix.
        """
        return self.board

    def copy(self):
        """
        Creates a deep copy of the board state.
        Used by solvers to avoid mutating shared boards.
        """
        new_board = NQueenBoard(self.n)
        new_board.board = [row[:] for row in self.board]
        new_board.queen_positions = self.queen_positions[:]
        new_board.col_conflicts = self.col_conflicts[:]
        new_board.diag1_conflicts = self.diag1_conflicts[:]
        new_board.diag2_conflicts = self.diag2_conflicts[:]
        new_board.move_count = self.move_count
        return new_board

    def get_move_count(self) -> int:
        """
        Returns the total number of moves made (for benchmarking).
        """
        return self.move_count

    def __eq__(self, other) -> bool:
        return self.board == other.board

    def __hash__(self) -> int:
        return hash(tuple(tuple(row) for row in self.board))
