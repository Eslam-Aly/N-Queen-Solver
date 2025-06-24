# N-Queens Problem: Algorithmic Comparison

This project presents a structured comparison of four distinct algorithmic strategies for solving the classic N-Queens problem:

- **Depth-First Search (DFS)**
- **Hill Climbing (HC)**
- **Simulated Annealing (SA)**
- **Genetic Algorithm (GA)**

The goal is to place N queens on an N×N chessboard such that no two queens attack each other. This project evaluates the algorithms under uniform initial conditions and experimental constraints, allowing for a fair and reproducible comparison.

---

## 📌 Objectives

- Evaluate fundamentally different solving techniques under controlled settings.
- Benchmark performance on board sizes: **N = 10, 30, 50, 100, 200**.
- Log and compare metrics:  
  -  Success Rate  
  -  Runtime  
  -  Memory Usage  
  -  Move Count  
  -  Conflict Count

---

## 📁 Project Structure

<pre><code>
├── board.py                     # Generates board and tracks queen conflicts
├── dfs_solver.py                # DFS implementation
├── hill_climbing.py             # Hill Climbing with restarts
├── simulated_annealing.py       # SA with temperature schedule
├── genetic_algorithm.py         # GA with selection, crossover, and mutation
├── test.py                      # Main script to run all algorithms and export results
├── main.py                      # Test the board setup visually
├── n_queens_benchmark_results   # CSV file with performance logs
└── README.md                    # Project description (this file)
</code></pre>

## 🧪 Benchmarking Method

Each solver is evaluated on randomized board configurations per N value to ensure reliable and reproducible results.  
Initial states are uniformly generated across algorithms to maintain fairness.

**Metrics Recorded:**
- Total Solve Time  
- Peak Memory Usage  
- Success/Failure Rate  
- Number of Queen Moves  
- Final Conflict Count (if unsolved)

Results are stored in `n_queens_benchmark_results.csv` for further analysis and visualization.

---

## 📝 License

This project is released under the **Apache-2.0 License**.

---

## 🤝 Contributing

Suggestions, improvements, and pull requests are welcome.  
Please open an issue to discuss any major changes before submitting a PR.

---

## 👤 Author

Built by [Eslam Aly](https://github.com/Eslam-Aly)
