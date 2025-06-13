# main.py

from n_queen_board import NQueenBoard

def test_board(size, seed=None):
    print(f"\nTesting NQueenBoard with size = {size} and seed = {seed}...\n")
    board = NQueenBoard(size=size, seed=seed)
    board.display()
    print("Initial State (Queen Positions):", board.get_state())
    print("Conflict Count:", board.get_conflict_count())
    print("Is Goal State:", board.is_goal())
    print("=" * 40)

if __name__ == "__main__":
    test_sizes = [10, 30, 50]
    for i, size in enumerate(test_sizes):
        test_board(size=size, seed=42)  # You can vary the seed for different runs