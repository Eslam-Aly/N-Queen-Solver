from dfs_solver import solve_n_queens_dfs
from hill_climbing_solver import solve_n_queens_hill_climbing
from sim_annealing_solver import solve_n_queens_simulated_annealing
from genetic_solver import solve_n_queens_genetic

def run_tests():
    algorithms = {
        "DFS": solve_n_queens_dfs,
        "Hill Climbing": solve_n_queens_hill_climbing,
        "Simulated Annealing": solve_n_queens_simulated_annealing,
        "Genetic Algorithm": solve_n_queens_genetic
    }

    n_values = [200]

    for n in n_values:
        print(f"\n==================== N = {n} ====================")
        for name, solver in algorithms.items():
            print(f"\n{name}:")
            result = solver(n)
            print(f"  ✅ Success       : {result['success']}")
            print(f"  ⏱️ Time (sec)     : {result['time']:.4f}")
            print(f"  🧠 Memory (MB)    : {result['memory_mb']:.2f}")
            print(f"  🔁 Moves         : {result['moves']}")
            print(f"  ❌ Conflicts     : {result['conflicts']}")
            if result["success"]:
                print("  🧩 Final board:")
                result["board"].print_board()

if __name__ == "__main__":
    run_tests()