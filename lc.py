import time
import random
import math
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

def SHC(start_state, goal_state):
    def hill_climbing(start_state, goal_state):
        start_time = time.time()
        current_state = start_state
        path = [start_state]
        visited = set()
        visited.add(state_to_tuple(start_state))
        nodes_expanded = 0

        while True:
            neighbors = generate_neighbors(current_state)
            nodes_expanded += 1

            if not neighbors:
                break

            next_state = min(neighbors, key=lambda state: manhattan_distance(state, goal_state))

            if manhattan_distance(next_state, goal_state) >= manhattan_distance(current_state, goal_state):
                break

            current_state = next_state
            path.append(current_state)
            visited.add(state_to_tuple(current_state))

            if current_state == goal_state:
                break

        end_time = time.time()
        return {
            "path": path if current_state == goal_state else None,
            "time": end_time - start_time,
            "nodes_expanded": nodes_expanded,
            "depth": len(path) - 1,
            "length": len(path) if current_state == goal_state else 0
        }

    return hill_climbing(start_state, goal_state)

def Stochastic(start_state, goal_state):
    start_time = time.time()
    nodes_expanded = 0

    def stochastic_hill_climbing(start_state, goal_state):
        nonlocal nodes_expanded
        current_state = start_state
        path = [start_state]

        while True:
            neighbors = generate_neighbors(current_state)
            nodes_expanded += len(neighbors)
            if not neighbors:
                break
            
            better_neighbors = [state for state in neighbors if manhattan_distance(state, goal_state) < manhattan_distance(current_state, goal_state)]
            if not better_neighbors:
                break
            
            current_state = random.choice(better_neighbors)
            path.append(current_state)

        return path if current_state == goal_state else None

    path = stochastic_hill_climbing(start_state, goal_state)
    end_time = time.time()

    return {
        "path": path,
        "time": end_time - start_time,
        "nodes_expanded": nodes_expanded,
        "depth": len(path)-1 if path else 0,
        "length": len(path) if path else 0
    }

def SAHC(start_state, goal_state):
    start_time = time.time()
    nodes_expanded = 0

    def steepest_ascent_hill_climbing(start_state, goal_state):
        nonlocal nodes_expanded
        current_state = start_state
        path = [start_state]

        while True:
            neighbors = generate_neighbors(current_state)
            nodes_expanded += len(neighbors)
            if not neighbors:
                break

            best_neighbor = min(neighbors, key=lambda s: manhattan_distance(s, goal_state))
            if manhattan_distance(best_neighbor, goal_state) >= manhattan_distance(current_state, goal_state):
                break

            current_state = best_neighbor
            path.append(current_state)

        return path if current_state == goal_state else None

    path = steepest_ascent_hill_climbing(start_state, goal_state)
    end_time = time.time()

    return {
        "path": path,
        "time": end_time - start_time,
        "nodes_expanded": nodes_expanded,
        "depth": len(path)-1 if path else 0,
        "length": len(path) if path else 0
    }

def SA(start_state, goal_state, initial_temp=100, cooling_rate=0.99, min_temp=0.1):
    start_time = time.time()
    current_state = start_state
    current_temp = initial_temp
    path = [start_state]
    nodes_expanded = 0

    while current_temp > min_temp:
        neighbors = generate_neighbors(current_state)
        nodes_expanded += len(neighbors)
        if not neighbors:
            break

        next_state = random.choice(neighbors)

        current_energy = manhattan_distance(current_state, goal_state)
        next_energy = manhattan_distance(next_state, goal_state)
        delta_energy = next_energy - current_energy

        if delta_energy < 0 or random.uniform(0, 1) < math.exp(-delta_energy / current_temp):
            current_state = next_state
            path.append(current_state)

        if current_state == goal_state:
            end_time = time.time()
            return {
                "path": path,
                "time": end_time - start_time,
                "nodes_expanded": nodes_expanded,
                "depth": len(path) - 1,
                "length": len(path)
            }

        current_temp *= cooling_rate

    end_time = time.time()
    return {
        "path": path if current_state == goal_state else None,
        "time": end_time - start_time,
        "nodes_expanded": nodes_expanded,
        "depth": len(path)-1 if path else 0,
        "length": len(path) if path else 0
    }
def BS(start_state, goal_state, beam_width=2):
    from heapq import heappush, heappop
    start_time = time.time()
    frontier = [(manhattan_distance(start_state, goal_state), start_state, [])]
    visited = set()
    visited.add(state_to_tuple(start_state))
    nodes_expanded = 0

    while frontier:
        new_frontier = []
        for _, current_state, path in frontier:
            if current_state == goal_state:
                end_time = time.time()
                full_path = [start_state] + path
                return {
                    "path": full_path,
                    "time": end_time - start_time,
                    "nodes_expanded": nodes_expanded,
                    "depth": len(full_path) - 1,
                    "length": len(full_path)
                }

            for neighbor in generate_neighbors(current_state):
                neighbor_tuple = state_to_tuple(neighbor)
                if neighbor_tuple not in visited:
                    visited.add(neighbor_tuple)
                    nodes_expanded += 1
                    heappush(new_frontier, (manhattan_distance(neighbor, goal_state), neighbor, path + [neighbor]))

        frontier = [heappop(new_frontier) for _ in range(min(beam_width, len(new_frontier)))]

    end_time = time.time()
    return {
        "path": None,
        "time": end_time - start_time,
        "nodes_expanded": nodes_expanded,
        "depth": 0,
        "length": 0
    }
def GEN(start_state, goal_state):
    import copy
    start_time = time.time()
    moves = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    def apply_moves(state, move_seq):
        current = copy.deepcopy(state)
        path_states = [copy.deepcopy(current)]
        for move in move_seq:
            x, y = find_zero(current)
            dx, dy = moves[move]
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                current[x][y], current[nx][ny] = current[nx][ny], current[x][y]
                path_states.append(copy.deepcopy(current))
            else:
                break
        return current, path_states

    def generate_random_moves(length):
        return [random.choice(list(moves.keys())) for _ in range(length)]

    def mutate(path):
        path = path[:]
        if random.random() < 0.3 and path:
            path.pop(random.randint(0, len(path)-1))
        if random.random() < 0.5:
            path.insert(random.randint(0, len(path)), random.choice(list(moves.keys())))
        if random.random() < 0.4 and path:
            path[random.randint(0, len(path)-1)] = random.choice(list(moves.keys()))
        return path

    def crossover(p1, p2):
        if not p1 or not p2:
            return p1 or p2
        cut = random.randint(1, min(len(p1), len(p2)) - 1)
        return p1[:cut] + p2[cut:]

    def fitness(state):
        return manhattan_distance(state, goal_state)

    def tiles_in_place(state):
        return sum(1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] == goal_state[i][j])

    def GA(start, goal, pop_size=50, generations=300, beam_width=5):
        population = [generate_random_moves(20) for _ in range(pop_size)]

        for gen in range(generations):
            scored = []
            seen = set()

            for path in population:
                end_state, path_states = apply_moves(start, path)
                tup = state_to_tuple(end_state)
                if tup in seen:
                    continue
                seen.add(tup)

                score = fitness(end_state)
                bonus = tiles_in_place(end_state)
                total_score = score - bonus * 0.5
                scored.append((total_score, path, path_states, end_state))

                if end_state == goal:
                    end_time = time.time()
                    return {
                        "path": path_states,
                        "time": end_time - start_time,
                        "nodes_expanded": len(seen),
                        "depth": len(path_states) - 1,
                        "length": len(path_states)
                    }

            scored.sort(key=lambda x: x[0])
            next_gen = [scored[i][1] for i in range(min(beam_width, len(scored)))]

            while len(next_gen) < pop_size:
                p1 = random.choice(scored[:beam_width])[1]
                p2 = random.choice(scored[:beam_width])[1]
                child = crossover(p1, p2)
                child = mutate(child)
                next_gen.append(child)

            population = next_gen

        end_time = time.time()
        return {
            "path": None,
            "time": end_time - start_time,
            "nodes_expanded": len(seen),
            "depth": 0,
            "length": 0
        }

    return GA(start_state, goal_state)
import matplotlib.pyplot as plt

start_state = [[2, 6, 5],
         [0, 8, 7],
         [4, 3, 1]]

goal_state = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]]

algorithms = {
    "SHC": SHC,
    "SAHC": SAHC,
    "Stochastic": Stochastic,
    "SA": SA,
    "Beam": BS,
    "GEN": GEN
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
    print(f"{algo:<20} | {data['time']:<12.5f} | {data['nodes_expanded']:<14} | {data['depth']:<7} | {data['length']:<15}")

# Lấy dữ liệu
algorithms = list(results.keys())
times = [results[algo]["time"] for algo in algorithms]
nodes_expanded = [results[algo]["nodes_expanded"] for algo in algorithms]
depths = [results[algo]["depth"] for algo in algorithms]
lengths = [results[algo]["length"] for algo in algorithms]

# Vẽ biểu đồ
plt.figure(figsize=(16, 10))
bar_width = 0.6
colors = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc949', '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab']

# Thời gian thực thi
plt.subplot(2, 2, 1)
plt.bar(algorithms, times, color=colors)
plt.title('Thời gian (s)')
plt.ylabel('Giây')
plt.xticks(rotation=45, ha='right')

# Node mở rộng
plt.subplot(2, 2, 2)
plt.bar(algorithms, nodes_expanded, color=colors)
plt.title('Số node mở rộng')
plt.ylabel('Số lượng')
plt.xticks(rotation=45, ha='right')

# Độ sâu
plt.subplot(2, 2, 3)
plt.bar(algorithms, depths, color=colors)
plt.title('Độ sâu lời giải')
plt.ylabel('Bước')
plt.xticks(rotation=45, ha='right')

# Độ dài lời giải
plt.subplot(2, 2, 4)
plt.bar(algorithms, lengths, color=colors)
plt.title('Độ dài lời giải')
plt.ylabel('Số bước')
plt.xticks(rotation=45, ha='right')

plt.suptitle('So sánh hiệu suất các thuật toán Local Search', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
