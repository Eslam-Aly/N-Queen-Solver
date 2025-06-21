import random
import time
import tracemalloc
from board import NQueenBoard

def count_conflicts(queen_cols):
    conflicts = 0
    n = len(queen_cols)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(queen_cols[i] - queen_cols[j]):
                conflicts += 1
    return conflicts

def get_best_swap(queen_cols):
    n = len(queen_cols)
    current_conflicts = count_conflicts(queen_cols)
    best_conflicts = current_conflicts
    best_swap = None

    for i in range(n):
        for j in range(i + 1, n):
            queen_cols[i], queen_cols[j] = queen_cols[j], queen_cols[i]
            new_conflicts = count_conflicts(queen_cols)
            queen_cols[i], queen_cols[j] = queen_cols[j], queen_cols[i]

            if new_conflicts < best_conflicts:
                best_conflicts = new_conflicts
                best_swap = (i, j)

    return best_swap, best_conflicts

def solve_n_queens_hill_climbing(n, seed=None, max_restarts=100, max_sideways=100):
    if seed is not None:
        random.seed(seed)

    move_count_total = 0
    restart_count = 0
    success = False
    best_board = None

    tracemalloc.start()
    start_time = time.perf_counter()

    while restart_count < max_restarts:
        # Start with a random valid permutation
        queen_cols = random.sample(range(n), n)
        move_count = 0
        sideways_moves = 0

        while True:
            conflicts = count_conflicts(queen_cols)
            if conflicts == 0:
                success = True
                break

            swap, new_conflicts = get_best_swap(queen_cols)

            if not swap:
                break  # Local minimum, no better swap found

            if new_conflicts < conflicts:
                sideways_moves = 0
            elif new_conflicts == conflicts:
                sideways_moves += 1
                if sideways_moves > max_sideways:
                    break
            else:
                break

            i, j = swap
            queen_cols[i], queen_cols[j] = queen_cols[j], queen_cols[i]
            move_count += 1

        move_count_total += move_count

        if success:
            # Build board for printing/visualization
            board = NQueenBoard(n)
            board.reset_board()
            for row, col in enumerate(queen_cols):
                board.board[row][col] = 1
                board.queen_positions.append((row, col))
            best_board = board
            break

        restart_count += 1

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": "HillClimbing+Swaps",
        "n": n,
        "time": round(end_time - start_time, 4),
        "memory_mb": round(peak / (1024 * 1024), 4),
        "success": success,
        "conflicts": 0 if success else count_conflicts(queen_cols),
        "moves": move_count_total,
        "restarts": restart_count,
        "max_restarts_reached": not success,
        "board": best_board
    }

# Example run
if __name__ == "__main__":
    n = 10
    print(f"Solving N = {n}")
    result = solve_n_queens_hill_climbing(n)
    print(f"N = {result['n']}, Success: {result['success']}, Time: {result['time']}s, "
          f"Moves: {result['moves']}, Restarts: {result['restarts']}, "
          f"Memory: {result['memory_mb']:.2f}MB")

    if result["success"]:
        result["board"].print_board()