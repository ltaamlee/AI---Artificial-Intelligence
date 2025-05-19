from collections import deque
from queue import PriorityQueue
import time
import matplotlib.pyplot as plt

# Tìm ô trống trên puzzle
def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

# Lưu trạng thái thành tuple để lưu vào set/dict
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

# BFS
def BFS(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set([state_to_tuple(start_state)])
    nodes_expanded = 0

    while queue:
        current, path = queue.popleft()
        nodes_expanded += 1

        if current == goal_state:
            return [start_state] + path, nodes_expanded

        zero_pos = find_zero(current)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            new_i, new_j = zero_pos[0] + move[0], zero_pos[1] + move[1]
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in current]
                new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]
                new_state_tuple = state_to_tuple(new_state)
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    queue.append((new_state, path + [new_state]))

    return None, nodes_expanded

# DFS với max_depth và đếm nodes mở rộng
def DFS(start_state, goal_state, max_depth=50):
    stack = [(start_state, [])]
    visited = set([state_to_tuple(start_state)])
    nodes_expanded = 0

    while stack:
        current, path = stack.pop()
        nodes_expanded += 1

        if current == goal_state:
            return [start_state] + path, nodes_expanded

        if len(path) >= max_depth:
            continue

        zero_pos = find_zero(current)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            new_i, new_j = zero_pos[0] + move[0], zero_pos[1] + move[1]
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in current]
                new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]
                new_state_tuple = state_to_tuple(new_state)
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    stack.append((new_state, path + [new_state]))

    return None, nodes_expanded

# UCS (Uniform Cost Search)
def UCS(start_state, goal_state):
    frontier = PriorityQueue()
    frontier.put((0, start_state, []))
    visited = {state_to_tuple(start_state): 0}
    nodes_expanded = 0

    while not frontier.empty():
        cost, current, path = frontier.get()
        nodes_expanded += 1

        if current == goal_state:
            return [start_state] + path, nodes_expanded

        zero_pos = find_zero(current)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            new_i, new_j = zero_pos[0] + move[0], zero_pos[1] + move[1]
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in current]
                new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]
                new_cost = cost + 1
                new_state_tuple = state_to_tuple(new_state)

                if new_state_tuple not in visited or new_cost < visited[new_state_tuple]:
                    visited[new_state_tuple] = new_cost
                    frontier.put((new_cost, new_state, path + [new_state]))

    return None, nodes_expanded

# DLS cho IDS
def DLS(current, goal_state, depth, path=None, visited=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()

    state_tuple = state_to_tuple(current)
    if state_tuple in visited:
        return None
    visited.add(state_tuple)

    if current == goal_state:
        return [current]

    if depth == 0:
        return None

    zero_pos = find_zero(current)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for move in moves:
        new_i, new_j = zero_pos[0] + move[0], zero_pos[1] + move[1]
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = [row[:] for row in current]
            new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]

            result = DLS(new_state, goal_state, depth - 1, path + [new_state], visited.copy())
            if result is not None:
                return [current] + result

    return None

# IDS gọi DLS và đếm nodes
def IDS(start_state, goal_state, max_depth=50):
    total_nodes_expanded = 0

    for depth in range(1, max_depth + 1):
        visited = set()
        nodes_expanded = 0

        # wrapper đếm nodes cho DLS
        def DLS_count(current, goal_state, depth, path=None):
            nonlocal nodes_expanded
            if path is None:
                path = []
            state_tuple = state_to_tuple(current)
            if state_tuple in visited:
                return None
            visited.add(state_tuple)
            nodes_expanded += 1

            if current == goal_state:
                return [current]
            if depth == 0:
                return None

            zero_pos = find_zero(current)
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for move in moves:
                new_i, new_j = zero_pos[0] + move[0], zero_pos[1] + move[1]
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = [row[:] for row in current]
                    new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]
                    result = DLS_count(new_state, goal_state, depth - 1, path + [new_state])
                    if result is not None:
                        return [current] + result
            return None

        result = DLS_count(start_state, goal_state, depth)
        total_nodes_expanded += nodes_expanded
        if result is not None:
            return result, total_nodes_expanded

    return None, total_nodes_expanded

# Hàm chạy thuật toán và thu thập kết quả
def run_search(algorithm, start_state, goal_state, max_depth=None):
    start_time = time.time()
    if max_depth is not None:
        path, nodes_expanded = algorithm(start_state, goal_state, max_depth)
    else:
        path, nodes_expanded = algorithm(start_state, goal_state)
    end_time = time.time()

    if path is None:
        return None

    elapsed_time = end_time - start_time
    path_length = len(path) - 1
    depth = path_length

    return {
        "time": elapsed_time,
        "nodes_expanded": nodes_expanded,
        "depth": depth,
        "length": path_length
    }

# State mẫu test
start = [[2, 6, 5],
         [0, 8, 7],
         [4, 3, 1]]

goal = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]]

# Chạy các thuật toán
results = {}
for algo in [BFS, DFS, UCS, IDS]:
    if algo == DFS or algo == IDS:
        res = run_search(algo, start, goal, max_depth=50)
    else:
        res = run_search(algo, start, goal)
    if res is not None:
        results[algo.__name__] = res
    else:
        print(f"{algo.__name__}: Không tìm thấy lời giải")

# Vẽ biểu đồ so sánh hiệu suất
algorithms = list(results.keys())
times = [results[algo]["time"] for algo in algorithms]
nodes_expanded = [results[algo]["nodes_expanded"] for algo in algorithms]
depths = [results[algo]["depth"] for algo in algorithms]
lengths = [results[algo]["length"] for algo in algorithms]
print("So sánh hiệu suất các thuật toán tìm kiếm 8-puzzle:\n")
print(f"{'Thuật toán':<10} | {'Thời gian (s)':<12} | {'Node mở rộng':<12} | {'Độ sâu':<7} | {'Độ dài lời giải':<15}")
print("-"*65)

for algo, data in results.items():
    print(f"{algo:<10} | {data['time']:<12.5f} | {data['nodes_expanded']:<12} | {data['depth']:<7} | {data['length']:<15}")

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.bar(algorithms, times, color='blue')
plt.title('Thời gian (s)')
plt.ylabel('Giây')

plt.subplot(2, 2, 2)
plt.bar(algorithms, nodes_expanded, color='red')
plt.title('Số node mở rộng')

plt.subplot(2, 2, 3)
plt.bar(algorithms, depths, color='green')
plt.title('Độ sâu lời giải')
plt.ylabel('Số bước')

plt.subplot(2, 2, 4)
plt.bar(algorithms, lengths, color='orange')
plt.title('Độ dài lời giải')

plt.suptitle('So sánh hiệu suất các thuật toán Uniformed Search', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
