# main.py

from board import NQueenBoard

def test_board(size, seed=None):
    print(f"\nTesting NQueenBoard with size = {size} and seed = {seed}...\n")
    board = NQueenBoard(n=size, seed=seed)  # ✅ Fixed here
    board.print_board()
    print("Initial State (Queen Positions):", board.get_positions())
    print("Conflict Count:", board.calculate_conflicts())
    print("Board Resetting...")
    board.reset_board()
    board.print_board()
    print("=" * 40)

if __name__ == "__main__":
    test_sizes = [10, 30, 50]
    for i, size in enumerate(test_sizes):
        test_board(size=size, seed=42)