import random
import time
import tracemalloc
from board import NQueenBoard

def create_individual(n):
    """Create an individual as a permutation of columns (1 queen per row)."""
    return random.sample(range(n), n)

def count_conflicts(individual):
    """Count diagonal conflicts in the individual (row = index, col = value)."""
    conflicts = 0
    for i in range(len(individual)):
        for j in range(i + 1, len(individual)):
            if abs(i - j) == abs(individual[i] - individual[j]):
                conflicts += 1
    return conflicts

def fitness(individual):
    """Higher fitness is better (fewer conflicts)."""
    return 1 / (1 + count_conflicts(individual))

def is_solution(individual):
    return count_conflicts(individual) == 0

def individual_to_board(individual):
    """Convert individual to NQueenBoard."""
    board = NQueenBoard(len(individual))
    board.reset_board()
    for row, col in enumerate(individual):
        board.place_queen(row, col)
    return board

def crossover(parent1, parent2):
    """Partially Mapped Crossover (PMX)."""
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[start:end] = parent1[start:end]

    remaining = [gene for gene in parent2 if gene not in child[start:end]]
    idx = 0
    for i in range(n):
        if child[i] is None:
            child[i] = remaining[idx]
            idx += 1
    return child

def mutate(individual, mutation_rate):
    """Swap mutation."""
    n = len(individual)
    for _ in range(int(mutation_rate * n)):
        i, j = random.sample(range(n), 2)
        individual[i], individual[j] = individual[j], individual[i]

def solve_n_queens_genetic(
    n,
    seed=None,
    population_size=500,
    generations=5000,
    mutation_rate=0.1,
    elitism_k=10
):
    if seed is not None:
        random.seed(seed)

    tracemalloc.start()
    start_time = time.perf_counter()

    population = [create_individual(n) for _ in range(population_size)]
    move_count = 0
    success = False

    for gen in range(generations):
        population.sort(key=fitness, reverse=True)
        move_count += 1
        best = population[0]

        if is_solution(best):
            success = True
            break

        # Elitism
        next_gen = population[:elitism_k]

        # Crossover and mutation
        while len(next_gen) < population_size:
            p1, p2 = random.choices(population[:50], k=2)
            child = crossover(p1, p2)
            mutate(child, mutation_rate)
            next_gen.append(child)

        population = next_gen

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    best_board = individual_to_board(population[0])

    return {
        "algorithm": "GeneticAlgorithm",
        "n": n,
        "time": round(end_time - start_time, 4),
        "memory_mb": round(peak / (1024 * 1024), 4),
        "success": success,
        "conflicts": 0 if success else best_board.calculate_conflicts(),
        "moves": move_count,
        "board": best_board if success else None
    }

# Example test
if __name__ == "__main__":
        n = 10  # Change this to test different sizes
        print(f"Solving N = {n}")
        result = solve_n_queens_genetic(n)
        print(f"N = {result['n']}, Success: {result['success']}, Time: {result['time']}s, "
              f"Moves: {result['moves']}, Memory: {result['memory_mb']}MB")
        if result["success"]:
            result["board"].print_board()