import csv
import time

from dfs_solver import solve_n_queens_dfs
from hill_climbing_solver import solve_n_queens_hill_climbing
from sim_annealing_solver import solve_n_queens_simulated_annealing
from genetic_solver import solve_n_queens_genetic

def run_tests():
    solvers = [
        solve_n_queens_hill_climbing,
        solve_n_queens_simulated_annealing,
        solve_n_queens_genetic,
        solve_n_queens_dfs
    ]

    n_values = [10, 30, 50, 100, 200]
    num_runs_per_n = 1  # Increase for better benchmark
    output_file = "n_queens_benchmark_results.csv"

    headers = [
        "Algorithm", "N", "Run", "Success", "Timeout", "Time(s)",
        "Moves", "Memory(MB)", "Conflicts",
        "Restarts", "MaxRestartsHit",
        "Generations", "MaxGenerationsHit"
]

    total = len(solvers) * len(n_values) * num_runs_per_n
    current = 1

    with open(output_file, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for solver in solvers:
            for n in n_values:
                for run in range(1, num_runs_per_n + 1):
                    print(f"[{current}/{total}] Running {solver.__name__} | N = {n} | Run = {run}")
                    current += 1

                    try:
                        seed = int(time.time() * 1000) % 1_000_000
                        result = solver(n=n, seed=seed)

                        writer.writerow({
                            "Algorithm": result["algorithm"],
                            "N": result["n"],
                            "Run": run,
                            "Success": result["success"],
                            "Timeout": result.get("timeout", False),
                            "Time(s)": round(result["time"], 4),
                            "Moves": result["moves"],
                            "Memory(MB)": round(result["memory_mb"], 2),
                            "Conflicts": result["conflicts"],
                            "Restarts": result.get("restarts", ""),
                            "MaxRestartsHit": result.get("max_restarts_reached", ""),
                            "Generations": result.get("generations", ""),
                            "MaxGenerationsHit": result.get("max_generations_reached", "")
                        })

                    except Exception as e:
                        print(f"Error in {solver.__name__} for N = {n}, Run = {run}: {e}")
                        writer.writerow({
                            "Algorithm": solver.__name__,
                            "N": n,
                            "Run": run,
                            "Success": False,
                            "Timeout": "Error",
                            "Time(s)": "Error",
                            "Moves": "Error",
                            "Memory(MB)": "Error",
                            "Conflicts": "Error",
                            "Restarts": "Error",
                            "MaxRestartsHit": "Error"
                        })

    print("\nAll tests completed. Results saved to 'n_queens_benchmark_results.csv'")

if __name__ == "__main__":
    run_tests()