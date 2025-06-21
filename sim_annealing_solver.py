import random
import time
import tracemalloc
from board import NQueenBoard

def calculate_conflicts(positions):
    """Calculate the number of diagonal conflicts in the board."""
    conflicts = 0
    n = len(positions)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(positions[i] - positions[j]):
                conflicts += 1
    return conflicts

def get_neighbor(positions):
    """Generates a neighboring state by swapping two columns."""
    neighbor = positions[:]
    i, j = random.sample(range(len(neighbor)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def individual_to_board(individual):
    """Convert individual to NQueenBoard."""
    board = NQueenBoard(len(individual))
    board.reset_board()
    for row, col in enumerate(individual):
        board.place_queen(row, col)
    return board

def solve_n_queens_simulated_annealing(n, seed=None,
    max_steps=100000,
    initial_temperature=100.0,
    cooling_rate=0.003):
    
    if seed is not None:
        random.seed(seed)

    tracemalloc.start()
    start_time = time.perf_counter()

    current = list(range(n))
    random.shuffle(current)
    current_conflicts = calculate_conflicts(current)
    move_count = 0

    temperature = initial_temperature
    success = False

    for step in range(max_steps):
        if current_conflicts == 0:
            success = True
            break

        neighbor = get_neighbor(current)
        neighbor_conflicts = calculate_conflicts(neighbor)
        delta = neighbor_conflicts - current_conflicts

        if delta < 0 or random.random() < pow(2.718, -delta / temperature):
            current = neighbor
            current_conflicts = neighbor_conflicts

        temperature *= (1 - cooling_rate)
        move_count += 1

    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    board = individual_to_board(current)

    return {
        "algorithm": "SimulatedAnnealing",
        "n": n,
        "success": success,
        "time": round(end_time - start_time, 4),
        "memory_mb": round(peak_mem / (1024 * 1024), 4),
        "moves": move_count,
        "conflicts": 0 if success else board.calculate_conflicts(),
        "board": board if success else None
    }

# Example usage
if __name__ == "__main__":
        n = 10
        print(f"Solving N = {n}")
        result = solve_n_queens_simulated_annealing(n)
        print(f"N = {result['n']}, Success: {result['success']}, Time: {result['time']}s, "
              f"Moves: {result['moves']}, Memory: {result['memory_mb']}MB")
        if result["success"]:
            result["board"].print_board()