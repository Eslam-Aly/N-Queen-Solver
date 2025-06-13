import time
import tracemalloc
from n_queen_board import NQueenBoard

def is_safe(board, row, col, n):
    """
    Check if placing a queen at (row, col) is safe.
    """
    for i in range(row):
        if board[i][col] == 1:
            return False
        if col - (row - i) >= 0 and board[i][col - (row - i)] == 1:
            return False
        if col + (row - i) < n and board[i][col + (row - i)] == 1:
            return False
    return True

def dfs_util(board_obj, row, move_counter):
    """
    Recursive utility to place queens row by row.
    Each valid attempt to place a queen counts as a move.
    """
    if row == board_obj.n:
        return True

    for col in range(board_obj.n):
        move_counter[0] += 1  # Count each placement attempt

        if is_safe(board_obj.board, row, col, board_obj.n):
            board_obj.board[row][col] = 1
            board_obj.queen_positions.append((row, col))

            if dfs_util(board_obj, row + 1, move_counter):
                return True

            # Backtrack
            board_obj.board[row][col] = 0
            board_obj.queen_positions.pop()

    return False

def solve_n_queens_dfs(n):
    """
    Solves the N-Queens problem using Depth-First Search.
    Returns a dictionary with benchmark metrics.
    """
    board = NQueenBoard(n)
    board.reset_board()
    move_counter = [0]

    tracemalloc.start()
    start_time = time.perf_counter()

    success = dfs_util(board, 0, move_counter)

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": "DFS",
        "n": n,
        "time": end_time - start_time,
        "memory_mb": peak / (1024 * 1024),
        "success": success,
        "conflicts": 0 if success else board.calculate_conflicts(),
        "moves": move_counter[0],
        "board": board if success else None
    }

# Example test
if __name__ == "__main__":
    result = solve_n_queens_dfs(30)
    print(f"Success: {result['success']}, Time: {result['time']:.4f}s, Moves: {result['moves']}, Memory: {result['memory_mb']:.2f}MB")
    if result["success"]:
        result["board"].print_board()