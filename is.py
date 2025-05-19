from collections import deque
import copy
from heapq import heappop, heappush
from queue import PriorityQueue
import random
import math
import time
def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

# Lưu trạng thái thành tuple để lưu vào set/dict
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)
def generate_neighbors(current_state):
    neighbors = []
    x, y = find_zero(current_state)

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in current_state]  
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)

    return neighbors

def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                goal_pos = [(x, y) for x in range(3) for y in range(3) if goal_state[x][y] == state[i][j]][0]
                distance += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
    return distance

def heuristic(inital_state, goal_state):
    return sum(inital_state[i][j] != goal_state[i][j] and inital_state[i][j] != 0 for i in range(3) for j in range(3))

def ASTAR(start_state, goal_state):
    def cost(state):
        return manhattan_distance(state, goal_state)

    start_time = time.time()
    frontier = PriorityQueue()
    frontier.put((cost(start_state), 0, start_state, []))
    visited = {state_to_tuple(start_state): 0}
    node_count = 0

    while not frontier.empty():
        _, g, current, path = frontier.get()
        node_count += 1

        if current == goal_state:
            end_time = time.time()
            return {
                'path': [start_state] + path,
                'time': end_time - start_time,
                'nodes': node_count,
                'depth': g,
                'length': len(path) + 1
            }

        zero_pos = find_zero(current)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            new_i, new_j = zero_pos[0] + move[0], zero_pos[1] + move[1]
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in current]
                new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = \
                    new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]
                new_state_tuple = state_to_tuple(new_state)
                new_g = g + 1
                if new_state_tuple not in visited or new_g < visited[new_state_tuple]:
                    visited[new_state_tuple] = new_g
                    frontier.put((new_g + cost(new_state), new_g, new_state, path + [new_state]))

    return None

def GDS(start_state, goal_state):
    start_time = time.time()
    frontier = PriorityQueue()
    frontier.put((manhattan_distance(start_state, goal_state), start_state, []))
    visited = set()
    node_count = 0

    while not frontier.empty():
        _, current, path = frontier.get()
        node_count += 1

        if current == goal_state:
            end_time = time.time()
            return {
                'path': [start_state] + path,
                'time': end_time - start_time,
                'nodes': node_count,
                'depth': len(path),
                'length': len(path) + 1
            }

        visited.add(state_to_tuple(current))
        zero_pos = find_zero(current)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            new_i, new_j = zero_pos[0] + move[0], zero_pos[1] + move[1]
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in current]
                new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = \
                    new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]
                new_state_tuple = state_to_tuple(new_state)
                if new_state_tuple not in visited:
                    frontier.put((manhattan_distance(new_state, goal_state), new_state, path + [new_state]))

    return None
def IDAS(start_state, goal_state, max_iterations=1000):
    import time
    start_time = time.time()
    node_count = 0

    def search(state, g, threshold, path, iteration):
        nonlocal node_count
        if iteration > max_iterations:
            return float("inf"), None

        f = g + manhattan_distance(state, goal_state)
        if f > threshold:
            return f, None

        if state == goal_state:
            return f, path

        min_cost = float("inf")
        zero_pos = find_zero(state)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            new_i, new_j = zero_pos[0] + move[0], zero_pos[1] + move[1]
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in state]
                new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = \
                    new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]

                if path and state_to_tuple(new_state) == state_to_tuple(path[-1]):
                    continue

                node_count += 1
                new_cost, result = search(new_state, g + 1, threshold, path + [new_state], iteration + 1)
                if result is not None:
                    return new_cost, result
                min_cost = min(min_cost, new_cost)

        return min_cost, None

    threshold = manhattan_distance(start_state, goal_state)
    path = [start_state]
    iteration_count = 0

    while iteration_count < max_iterations:
        cost, result = search(start_state, 0, threshold, path, 0)
        if result is not None:
            end_time = time.time()
            return {
                'path': result,
                'time': end_time - start_time,
                'nodes': node_count,
                'depth': len(result) - 1,
                'length': len(result)
            }
        if cost == float("inf"):
            return None
        threshold = cost
        iteration_count += 1

    return None

import matplotlib.pyplot as plt

start_state = [[2, 6, 5],
         [0, 8, 7],
         [4, 3, 1]]

goal_state = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]]

algorithms = {
    "GDS": GDS,
    "A*": ASTAR,
    "IDAS":IDAS
}
results = {}
for name, algo in algorithms.items():
    print(f"Đang chạy: {name}")
    result = algo(start_state, goal_state)
    results[name] = result
    
# In bảng so sánh
print("So sánh hiệu suất các thuật toán tìm kiếm 8-puzzle:\n")
print(f"{'Thuật toán':<20} | {'Thời gian (s)':<12} | {'Node mở rộng':<14} | {'Độ sâu':<7} | {'Độ dài lời giải':<15}")
print("-" * 80)

for algo, data in results.items():
    print(f"{algo:<20} | {data['time']:<12.5f} | {data['nodes']:<14} | {data['depth']:<7} | {data['length']:<15}")

# Lấy dữ liệu
algorithms = list(results.keys())
times = [results[algo]["time"] for algo in algorithms]
nodes_expanded = [results[algo]["nodes"] for algo in algorithms]
depths = [results[algo]["depth"] for algo in algorithms]
lengths = [results[algo]["length"] for algo in algorithms]

# Vẽ biểu đồ
times = [results[k]["time"] for k in results]
nodes = [results[k]["nodes"] for k in results]
depths = [results[k]["depth"] for k in results]
lengths = [results[k]["length"] for k in results]

plt.figure(figsize=(16, 10))
labels = list(results.keys())
colors = ['#4e79a7', '#f28e2b', '#e15759']

plt.subplot(2, 2, 1)
plt.bar(labels, times, color=colors)
plt.title("Thời gian (s)")

plt.subplot(2, 2, 2)
plt.bar(labels, nodes, color=colors)
plt.title("Số node mở rộng")

plt.subplot(2, 2, 3)
plt.bar(labels, depths, color=colors)
plt.title("Độ sâu lời giải")

plt.subplot(2, 2, 4)
plt.bar(labels, lengths, color=colors)
plt.title("Độ dài lời giải")

plt.suptitle('So sánh hiệu suất các thuật toán Informed Search', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

plt.show()

