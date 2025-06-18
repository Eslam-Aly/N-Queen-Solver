import csv
import time

from dfs_solver import solve_n_queens_dfs
from hill_climbing_solver import solve_n_queens_hill_climbing
from restart_hill_climbing_solver import solve_n_queens_restart_hill_climbing
from sim_annealing_solver import solve_n_queens_simulated_annealing
from genetic_solver import solve_n_queens_genetic

# Define solvers
ALGORITHMS = [
    ("DFS", solve_n_queens_dfs),
    ("HillClimbing", solve_n_queens_hill_climbing),
    ("RestartHillClimbing", solve_n_queens_restart_hill_climbing),
    ("SimulatedAnnealing", solve_n_queens_simulated_annealing),
    ("GeneticAlgorithm", solve_n_queens_genetic),
]

N_SIZES = [10, 30, 50, 100, 200]
SEED = 42
TIMEOUT_LIMIT = 60  # seconds
CSV_FILE = "benchmark_results.csv"

TOTAL_TASKS = sum(
    1 for n in N_SIZES for name, _ in ALGORITHMS
    if not (name == "DFS" and n > 50) and not (name == "GeneticAlgorithm" and n > 100)
)
completed_tasks = 0

def safe_run(solver_func, n, seed):
    """
    Run solver function with timeout and return result or fallback if it fails.
    """
    try:
        if "dfs" in solver_func.__name__:
            return solver_func(n=n, timeout_sec=TIMEOUT_LIMIT)
        else:
            return solver_func(n=n, seed=seed)
    except Exception as e:
        return {
            "algorithm": solver_func.__name__,
            "n": n,
            "time": None,
            "memory_mb": None,
            "success": False,
            "conflicts": None,
            "moves": None,
            "board": None,
            "timeout": True,
            "error": str(e)
        }

def print_progress_bar(current, total, length=40):
    """
    Prints a simple text progress bar.
    """
    percent = int(100 * current / total)
    filled_len = int(length * current // total)
    bar = "=" * filled_len + "-" * (length - filled_len)
    print(f"\rProgress: [{bar}] {percent}% ({current}/{total})", end="")

def run_benchmark():
    global completed_tasks
    results = []

    print("Starting benchmark...\n")
    for n in N_SIZES:
        for name, solver in ALGORITHMS:
            if name == "DFS" and n > 50:
                completed_tasks += 1
                print_progress_bar(completed_tasks, TOTAL_TASKS)
                continue
            if name == "GeneticAlgorithm" and n > 100:
                completed_tasks += 1
                print_progress_bar(completed_tasks, TOTAL_TASKS)
                continue

            print(f"\nRunning {name} for N={n}...")
            result = safe_run(solver, n, SEED)

            results.append({
                "algorithm": result.get("algorithm", name),
                "n": result["n"],
                "success": result["success"],
                "time": result["time"],
                "memory_mb": result["memory_mb"],
                "moves": result["moves"],
                "conflicts": result["conflicts"],
                "timeout": result.get("timeout", False),
                "error": result.get("error", "")
            })

            completed_tasks += 1
            print_progress_bar(completed_tasks, TOTAL_TASKS)

    print("\n\nWriting results to CSV...")

    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "algorithm", "n", "success", "time", "memory_mb",
            "moves", "conflicts", "timeout", "error"
        ])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Benchmark completed and saved to {CSV_FILE}")

if __name__ == "__main__":
    run_benchmark()