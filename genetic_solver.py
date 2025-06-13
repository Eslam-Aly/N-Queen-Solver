import random
import time
import tracemalloc
from n_queen_board import NQueenBoard

def create_individual(n):
    """
    An individual is a list of column positions (1 queen per row).
    """
    return [random.randint(0, n - 1) for _ in range(n)]

def fitness(individual):
    """
    Return the number of non-conflicting pairs divided by total pairs.
    """
    n = len(individual)
    total_pairs = n * (n - 1) // 2
    non_conflicts = 0

    for i in range(n):
        for j in range(i + 1, n):
            if individual[i] != individual[j] and abs(i - j) != abs(individual[i] - individual[j]):
                non_conflicts += 1

    return non_conflicts / total_pairs  # Normalized

def is_solution(individual):
    return fitness(individual) == 1.0

def individual_to_board(individual):
    n = len(individual)
    board = NQueenBoard(n)
    board.reset_board()
    for row in range(n):
        col = individual[row]
        board.board[row][col] = 1
        board.queen_positions.append((row, col))
    return board

def crossover(p1, p2):
    n = len(p1)
    point = random.randint(1, n - 2)
    return p1[:point] + p2[point:]

def mutate(individual, mutation_rate):
    n = len(individual)
    for i in range(n):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, n - 1)

def solve_n_queens_genetic(n, seed=None,
                           population_size=100,
                           generations=1000,
                           mutation_rate=0.02,
                           selection_size=20):
    """
    Solve N-Queens using Genetic Algorithm.
    Returns a dictionary with benchmarking metrics.
    """
    if seed is not None:
        random.seed(seed)

    population = [create_individual(n) for _ in range(population_size)]
    move_count = 0  # Each generation counts as a "move"

    tracemalloc.start()
    start_time = time.perf_counter()

    for gen in range(generations):
        population.sort(key=fitness, reverse=True)
        move_count += 1

        if is_solution(population[0]):
            board = individual_to_board(population[0])
            success = True
            break

        next_gen = population[:selection_size]  # Elitism

        while len(next_gen) < population_size:
            parent1 = random.choice(population[:selection_size])
            parent2 = random.choice(population[:selection_size])
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            next_gen.append(child)

        population = next_gen

    else:
        success = False
        board = individual_to_board(population[0])

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": "GeneticAlgorithm",
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
    result = solve_n_queens_genetic(30, seed=42)
    print(f"Success: {result['success']}, Time: {result['time']:.4f}s, Moves: {result['moves']}, Memory: {result['memory_mb']:.2f}MB")
    if result["success"]:
        result["board"].print_board()