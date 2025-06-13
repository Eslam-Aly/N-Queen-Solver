import math
import random
import time
import tracemalloc
from n_queen_board import NQueenBoard

def get_neighbor(board_obj):
    """
    Generate a neighboring state by moving one queen to a new column in the same row.
    """
    n = board_obj.n
    row = random.randint(0, n - 1)
    current_col = board_obj.queen_positions[row][1]
    new_col = random.choice([c for c in range(n) if c != current_col])

    neighbor = board_obj.copy()
    neighbor.board[row][current_col] = 0
    neighbor.board[row][new_col] = 1
    neighbor.queen_positions[row] = (row, new_col)

    return neighbor

def acceptance_probability(current_conflicts, neighbor_conflicts, temperature):
    """
    Probability of accepting a worse move based on temperature.
    """
    if neighbor_conflicts < current_conflicts:
        return 1.0
    return math.exp((current_conflicts - neighbor_conflicts) / temperature)

def solve_n_queens_simulated_annealing(n, seed=None,
                                       initial_temp=1000.0,
                                       cooling_rate=0.003,
                                       max_iterations=100000):
    """
    Solve N-Queens using Simulated Annealing.
    Returns a dictionary with benchmarking metrics.
    """
    if seed is not None:
        random.seed(seed)

    board = NQueenBoard(n, seed)
    current_conflicts = board.calculate_conflicts()
    temperature = initial_temp
    move_count = 0

    tracemalloc.start()
    start_time = time.perf_counter()

    for i in range(max_iterations):
        if current_conflicts == 0:
            success = True
            break

        neighbor = get_neighbor(board)
        neighbor_conflicts = neighbor.calculate_conflicts()
        move_count += 1

        if acceptance_probability(current_conflicts, neighbor_conflicts, temperature) > random.random():
            board = neighbor
            current_conflicts = neighbor_conflicts

        temperature *= (1 - cooling_rate)
        if temperature < 1e-6:
            success = False
            break
    else:
        success = False

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": "SimulatedAnnealing",
        "n": n,
        "time": end_time - start_time,
        "memory_mb": peak / (1024 * 1024),
        "success": success,
        "conflicts": 0 if success else board.calculate_conflicts(),
        "moves": move_count,
        "board": board if success else None
    }

# Example test
if __name__ == "__main__":
    result = solve_n_queens_simulated_annealing(30, seed=42)
    print(f"Success: {result['success']}, Time: {result['time']:.4f}s, Moves: {result['moves']}, Memory: {result['memory_mb']:.2f}MB")
    if result["success"]:
        result["board"].print_board()