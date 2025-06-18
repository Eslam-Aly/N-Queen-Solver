import random
import time
import tracemalloc
from multiprocessing import Process, Queue
from n_queen_board import NQueenBoard

def create_individual(n):
    """
    An individual is a permutation of [0..n-1] representing column positions.
    Each value at index `i` means the queen in row `i` is placed in that column.
    This avoids row and column conflicts by design.
    """
    return random.sample(range(n), n)

def count_conflicts(individual):
    """
    Count diagonal conflicts in an individual.
    """
    n = len(individual)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(individual[i] - individual[j]):
                conflicts += 1
    return conflicts

def fitness(individual):
    """
    Fitness is inverse of the number of diagonal conflicts.
    """
    return 1 / (1 + count_conflicts(individual))

def is_solution(individual):
    return count_conflicts(individual) == 0

def individual_to_board(individual):
    n = len(individual)
    board = NQueenBoard(n)
    board.reset_board()
    for row, col in enumerate(individual):
        board.board[row][col] = 1
        board.queen_positions.append((row, col))
    return board

def crossover(parent1, parent2):
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[start:end] = parent1[start:end]
    fill = [x for x in parent2 if x not in child[start:end]]
    idx = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child

def mutate(individual, mutation_rate):
    n = len(individual)
    for i in range(n):
        if random.random() < mutation_rate:
            j = random.randint(0, n - 1)
            individual[i], individual[j] = individual[j], individual[i]

def genetic_algorithm_worker(n, seed, queue, population_size=100, generations=1000,
                              mutation_rate=0.1, elitism_k=5):
    if seed is not None:
        random.seed(seed)

    population = [create_individual(n) for _ in range(population_size)]
    move_count = 0

    tracemalloc.start()
    start_time = time.perf_counter()

    for gen in range(generations):
        population.sort(key=fitness, reverse=True)
        move_count += 1

        if is_solution(population[0]):
            board = individual_to_board(population[0])
            success = True
            break

        next_gen = population[:elitism_k]

        while len(next_gen) < population_size:
            p1, p2 = random.choices(population[:50], k=2)
            child = crossover(p1, p2)
            mutate(child, mutation_rate)
            next_gen.append(child)

        population = next_gen

    else:
        success = False
        board = individual_to_board(population[0])

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    queue.put({
        "algorithm": "GeneticAlgorithm",
        "n": n,
        "time": end_time - start_time,
        "memory_mb": peak / (1024 * 1024),
        "success": success,
        "conflicts": 0 if success else board.calculate_conflicts(),
        "moves": move_count,
        "board": board if success else None
    })

def solve_n_queens_genetic(n, seed=None, timeout_seconds=30):
    queue = Queue()
    process = Process(target=genetic_algorithm_worker, args=(n, seed, queue))
    process.start()
    process.join(timeout_seconds)

    if process.is_alive():
        process.terminate()
        process.join()
        return {
            "algorithm": "GeneticAlgorithm",
            "n": n,
            "time": timeout_seconds,
            "memory_mb": 0,
            "success": False,
            "conflicts": -1,
            "moves": 0,
            "board": None
        }

    return queue.get()

# Example usage
if __name__ == "__main__":
    result = solve_n_queens_genetic(30, seed=42)
    print(f"Success: {result['success']}, Time: {result['time']:.4f}s, Moves: {result['moves']}, Memory: {result['memory_mb']:.2f}MB")
    if result["success"]:
        result["board"].print_board()
