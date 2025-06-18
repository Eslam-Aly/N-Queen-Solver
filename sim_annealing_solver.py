import random
import time
import tracemalloc
from n_queen_board import NQueenBoard

def calculate_conflicts(board_obj):
    return board_obj.calculate_conflicts()

def get_random_neighbor(board_obj):
    n = board_obj.n
    neighbor = board_obj.copy()
    row = random.randint(0, n - 1)
    current_col = neighbor.queen_positions[row][1]
    
    new_col = random.choice([c for c in range(n) if c != current_col])
    neighbor.board[row][current_col] = 0
    neighbor.board[row][new_col] = 1
    neighbor.queen_positions[row] = (row, new_col)
    return neighbor

def acceptance_probability(old_conflicts, new_conflicts, temperature):
    if new_conflicts < old_conflicts:
        return 1.0
    return pow(2.71828, -(new_conflicts - old_conflicts) / temperature)

def solve_n_queens_simulated_annealing(n, seed=None, initial_temp=100.0, cooling_rate=0.003, min_temp=0.01, max_steps=100000):
    if seed is not None:
        random.seed(seed)

    board = NQueenBoard(n, seed)
    move_count = 0

    tracemalloc.start()
    start_time = time.perf_counter()

    temperature = initial_temp

    for step in range(max_steps):
        current_conflicts = calculate_conflicts(board)
        if current_conflicts == 0:
            success = True
            break

        neighbor = get_random_neighbor(board)
        new_conflicts = calculate_conflicts(neighbor)

        if acceptance_probability(current_conflicts, new_conflicts, temperature) > random.random():
            board = neighbor

        temperature *= (1 - cooling_rate)
        if temperature < min_temp:
            break

        move_count += 1
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
        "conflicts": 0 if success else calculate_conflicts(board),
        "moves": move_count,
        "board": board if success else None
    }

# Example test
if __name__ == "__main__":
    result = solve_n_queens_simulated_annealing(30, seed=42)
    print(f"Success: {result['success']}, Time: {result['time']:.4f}s, Moves: {result['moves']}, Memory: {result['memory_mb']:.2f}MB")
    if result["success"]:
        result["board"].print_board()
