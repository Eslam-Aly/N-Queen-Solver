import time
import tracemalloc
from board import NQueenBoard

def is_safe(row, col, queens):
    for qr, qc in queens:
        if qc == col or abs(row - qr) == abs(col - qc):
            return False
    return True

def solve_n_queens_dfs(n, seed=None, timeout=600):
    """
    Solves the N-Queens problem using pure DFS with backtracking.
    No randomization, fair for benchmarking.
    """
    if seed is not None:
        import random
        random.seed(seed)
    board = NQueenBoard(n)
    board.reset_board()

    solution = []
    move_count = 0
    timed_out = False
    start_time = time.perf_counter()
    tracemalloc.start()

    def dfs(row, queens):
        nonlocal solution, move_count, timed_out

        # Timeout check
        if time.perf_counter() - start_time > timeout:
            timed_out = True
            return

        if row == n:
            solution.extend(queens)  # Copy final solution
            return

        for col in range(n):  # No shuffle — deterministic DFS
            if is_safe(row, col, queens):
                move_count += 1
                queens.append((row, col))
                dfs(row + 1, queens)
                if solution:
                    return
                queens.pop()

    dfs(0, [])

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if solution:
        for row, col in solution:
            board.place_queen(row, col)

    return {
        "algorithm": "DFS",
        "n": n,
        "success": bool(solution),
        "timeout": timed_out,
        "time": round(end_time - start_time, 4),
        "moves": move_count,
        "memory_mb": round(peak / (1024 * 1024), 4),
        "conflicts": board.calculate_conflicts() if solution else "N/A",
        "board": board if solution else None
    }

# Example test
if __name__ == "__main__":
    n = 10
    result = solve_n_queens_dfs(n, timeout=1200)
    print(f"N = {result['n']}, Success: {result['success']}, Timeout: {result['timeout']}, "
          f"Time: {result['time']}s, Moves: {result['moves']}, Memory: {result['memory_mb']}MB")
    if result["success"]:
        result["board"].print_board()