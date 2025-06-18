import random
import time
import tracemalloc
import multiprocessing
from n_queen_board import NQueenBoard

def calculate_conflicts(board_obj):
    return board_obj.calculate_conflicts()

def get_best_move_with_sideways(board_obj, allow_sideways=True):
    """
    Tries all possible queen moves and picks the best one (including sideways if allowed).
    Returns (row, new_col, new_conflicts) or None if stuck.
    """
    n = board_obj.n
    current_conflicts = calculate_conflicts(board_obj)
    best_moves = []
    best_conflicts = current_conflicts

    for row in range(n):
        current_col = board_obj.queen_positions[row][1]

        for new_col in range(n):
            if new_col == current_col:
                continue

            board_obj.board[row][current_col] = 0
            board_obj.board[row][new_col] = 1
            board_obj.queen_positions[row] = (row, new_col)

            new_conflicts = calculate_conflicts(board_obj)

            if new_conflicts < best_conflicts:
                best_conflicts = new_conflicts
                best_moves = [(row, new_col)]
            elif allow_sideways and new_conflicts == best_conflicts:
                best_moves.append((row, new_col))

            board_obj.board[row][new_col] = 0
            board_obj.board[row][current_col] = 1
            board_obj.queen_positions[row] = (row, current_col)

    if best_moves:
        return random.choice(best_moves), best_conflicts
    else:
        return None, current_conflicts

def restart_hill_climbing_worker(n, seed, max_steps, max_restarts, allow_sideways, result_dict):
    if seed is not None:
        random.seed(seed)

    move_count = 0
    tracemalloc.start()
    start_time = time.perf_counter()

    success = False
    board = None

    for restart in range(max_restarts):
        board = NQueenBoard(n, seed + restart if seed is not None else None)

        for step in range(max_steps):
            current_conflicts = calculate_conflicts(board)
            if current_conflicts == 0:
                success = True
                break

            move, new_conflicts = get_best_move_with_sideways(board, allow_sideways=allow_sideways)
            move_count += 1

            if move is None or new_conflicts >= current_conflicts:
                break  # Local minimum

            row, new_col = move
            old_col = board.queen_positions[row][1]
            board.board[row][old_col] = 0
            board.board[row][new_col] = 1
            board.queen_positions[row] = (row, new_col)

        if success:
            break

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result_dict.update({
        "algorithm": "HillClimbing_Restarts",
        "n": n,
        "time": end_time - start_time,
        "memory_mb": peak / (1024 * 1024),
        "success": success,
        "conflicts": 0 if success else calculate_conflicts(board),
        "moves": move_count,
        "board": board if success else None
    })

def solve_n_queens_restart_hill_climbing(n, seed=None, max_steps=1000, max_restarts=50, allow_sideways=True, timeout_sec=15):
    """
    Optimized Hill Climbing with Random Restarts and optional Sideways Moves.
    """
    manager = multiprocessing.Manager()
    result_dict = manager.dict()
    process = multiprocessing.Process(
        target=restart_hill_climbing_worker,
        args=(n, seed, max_steps, max_restarts, allow_sideways, result_dict)
    )

    process.start()
    process.join(timeout=timeout_sec)

    if process.is_alive():
        process.terminate()
        process.join()
        return {
            "algorithm": "HillClimbing_Restarts",
            "n": n,
            "time": timeout_sec,
            "memory_mb": None,
            "success": False,
            "conflicts": None,
            "moves": None,
            "board": None,
            "timeout": True
        }

    result_dict = dict(result_dict)
    result_dict["timeout"] = False
    return result_dict

# Example test
if __name__ == "__main__":
    result = solve_n_queens_restart_hill_climbing(30, seed=42)
    print(f"Success: {result['success']}, Time: {result['time']:.4f}s, Moves: {result['moves']}, Memory: {result['memory_mb']:.2f}MB")
    if result["success"] and result["board"]:
        result["board"].print_board()
