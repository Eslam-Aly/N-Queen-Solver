import random
import time
import tracemalloc
from n_queen_board import NQueenBoard

def calculate_conflicts(board_obj):
    """
    Count the number of conflicting pairs of queens.
    """
    return board_obj.calculate_conflicts()

def get_best_move(board_obj):
    """
    Try moving each queen in its row to a different column to find the best move.
    Returns (row, new_col, new_conflicts), or None if no better move found.
    """
    n = board_obj.n
    current_conflicts = calculate_conflicts(board_obj)
    best_move = None
    best_conflicts = current_conflicts

    for row in range(n):
        current_col = board_obj.queen_positions[row][1]

        for new_col in range(n):
            if new_col == current_col:
                continue

            # Try move
            board_obj.board[row][current_col] = 0
            board_obj.board[row][new_col] = 1
            board_obj.queen_positions[row] = (row, new_col)

            new_conflicts = calculate_conflicts(board_obj)

            if new_conflicts < best_conflicts:
                best_conflicts = new_conflicts
                best_move = (row, new_col)

            # Undo move
            board_obj.board[row][new_col] = 0
            board_obj.board[row][current_col] = 1
            board_obj.queen_positions[row] = (row, current_col)

    return best_move, best_conflicts

def solve_n_queens_hill_climbing(n, seed=None, max_steps=1000):
    """
    Solve N-Queens using Hill Climbing (fair version, no restarts).
    Returns a dictionary with benchmarking metrics.
    """
    if seed is not None:
        random.seed(seed)

    board = NQueenBoard(n, seed)
    move_count = 0

    tracemalloc.start()
    start_time = time.perf_counter()

    for step in range(max_steps):
        current_conflicts = calculate_conflicts(board)
        if current_conflicts == 0:
            success = True
            break

        move, new_conflicts = get_best_move(board)
        move_count += 1  # One move attempt per improvement

        if move is None or new_conflicts >= current_conflicts:
            success = False
            break

        # Apply move
        row, new_col = move
        old_col = board.queen_positions[row][1]
        board.board[row][old_col] = 0
        board.board[row][new_col] = 1
        board.queen_positions[row] = (row, new_col)

    else:
        success = False

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": "HillClimbing",
        "n": n,
        "time": end_time - start_time,
        "memory_mb": peak / (1024 * 1024),
        "success": success,
        "conflicts": 0 if success else calculate_conflicts(board),
        "moves": move_count,
        "board": board if success else None
    }

# Example test
if __name__ == "__main__":
    result = solve_n_queens_hill_climbing(30, seed=42)
    print(f"Success: {result['success']}, Time: {result['time']:.4f}s, Moves: {result['moves']}, Memory: {result['memory_mb']:.2f}MB")
    if result["success"]:
        result["board"].print_board()