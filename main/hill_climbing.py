import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv(r"main\dataset\borvo_HW_map.csv")

# Konversi ke grid dictionary
grid = {}
for _, row in df.iterrows():
    grid[(int(row["i"]), int(row["j"]))] = {"H": row["H"], "W": row["W"]}

# Fungsi ambil tetangga 8 arah (termasuk diagonal)
def get_all_neighbors(pos):
    i, j = pos
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]
    neighbors = [(i + di, j + dj) for di, dj in directions]
    return [n for n in neighbors if n in grid]

# Fungsi hitung skor W/E
def get_score(current_pos, neighbor_pos):
    H1 = grid[current_pos]["H"]
    H2 = grid[neighbor_pos]["H"]
    S = H1 - H2

    if S > 0.5:
        return -np.inf  # Tidak aman → skip

    E = 1 + 2 * abs(S)
    W = grid[neighbor_pos]["W"]
    return W / E

# Hill Climbing Algorithm
def hill_climbing_all_dirs(start):
    if start not in grid:
        print(f"Titik {start} tidak ditemukan dalam dataset.")
        return []

    current = start
    path = [current]
    current_score = grid[current]["W"] / (1 + 2 * abs(0))  # E = 1

    while True:
        neighbors = get_all_neighbors(current)
        scores = [(n, get_score(current, n)) for n in neighbors]
        valid_moves = [s for s in scores if s[1] > current_score]

        if not valid_moves:
            break  # local maximum reached

        # Pilih neighbor dengan skor tertinggi
        next_node, next_score = max(valid_moves, key=lambda x: x[1])
        path.append(next_node)
        current = next_node
        current_score = next_score

    return path

# Titik uji coba
test_points = [
    (540, 648),
    (20, 502),
    (588, 1000)
]

# Jalankan algoritma untuk semua titik uji
for idx, point in enumerate(test_points, 1):
    print(f"\n=== Titik {idx} - Start di {point} ===")
    path = hill_climbing_all_dirs(point)
    print(f"Jumlah langkah: {len(path)}")
    print("Jalur:")
    for p in path:
        print(p)
