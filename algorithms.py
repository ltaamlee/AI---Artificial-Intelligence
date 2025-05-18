from collections import deque
import copy
from heapq import heappop, heappush
from queue import PriorityQueue
import random
import math

# Tìm ô trống trên puzzle
def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

# Lưu trạng thái thành tuple
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)
#====================================================================================#

def BFS(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
        
    visited.add(state_to_tuple(start_state))
    while queue:
        current, path = queue.popleft()
        
        if current == goal_state:
            return [start_state] + path

        zero_pos = find_zero(current)
        
        # Up - Down - Left - Right
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
    
    return None

def DFS(start_state, goal_state, max_depth=1000):
    stack = [(start_state, [])]
    visited = set([state_to_tuple(start_state)])
    
    while stack:
        current, path = stack.pop()
        
        if current == goal_state:
            return [start_state] + path
            
        if len(path) >= max_depth:
            continue
            
        zero_pos = find_zero(current)
                
        # Up - Down - Left - Right
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
    
    return None

def UCS(start_state, goal_state):
    
    frontier = PriorityQueue()
    frontier.put((0, start_state, []))
    visited = {state_to_tuple(start_state): 0}
    
    while not frontier.empty():
        cost, current, path = frontier.get()
        
        if current == goal_state:
            return [start_state] + path
            
        zero_pos = find_zero(current)
                
        # Up - Down - Left - Right
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
    
    return None

def IDS(start_state, goal_state, max_depth=50):
    for depth in range(1, max_depth + 1):
        result = DLS(start_state, goal_state, depth)
        if result is not None:
            return result
    return None

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

#====================================================================================#

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

def GDS(start_state, goal_state):
    frontier = PriorityQueue()
    frontier.put((manhattan_distance(start_state, goal_state), start_state, []))
    visited = set()

    while not frontier.empty():
        _, current, path = frontier.get()

        if current == goal_state:
            return [start_state] + path

        visited.add(state_to_tuple(current))

        zero_pos = find_zero(current)
            
        # Up - Down - Left - Right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            new_i, new_j = zero_pos[0] + move[0], zero_pos[1] + move[1]

            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in current]
                new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]

                new_state_tuple = state_to_tuple(new_state)
                if new_state_tuple not in visited:
                    frontier.put((heuristic(new_state, goal_state), new_state, path + [new_state]))

    return None

def ASTAR(start_state, goal_state):
    def cost(state):
        return manhattan_distance(state, goal_state)

    frontier = PriorityQueue()
    frontier.put((cost(start_state), 0, start_state, []))
    visited = {state_to_tuple(start_state): 0}
    
    while not frontier.empty():
        _, g, current, path = frontier.get()
        
        if current == goal_state:
            return [start_state] + path
        
        zero_pos = find_zero(current)
        
        # Up - Down - Left - Right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for move in moves:
            new_i, new_j = zero_pos[0] + move[0], zero_pos[1] + move[1]
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in current]
                new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]
                new_state_tuple = state_to_tuple(new_state)
                new_g = g + 1
                if new_state_tuple not in visited or new_g < visited[new_state_tuple]:
                    visited[new_state_tuple] = new_g
                    frontier.put((new_g + cost(new_state), new_g, new_state, path + [new_state]))
    return None

def IDAS(start_state, goal_state, max_iterations=1000):
    
    def search(state, g, threshold, path, iteration):
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
                new_state[zero_pos[0]][zero_pos[1]], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_pos[0]][zero_pos[1]]
                
                if path and state_to_tuple(new_state) == state_to_tuple(path[-1]):
                    continue
                
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
            return result
        
        if cost == float("inf"):
            return None
        
        threshold = cost
        iteration_count += 1
    
    return None

#====================================================================================#
def SHC(start_state, goal_state):

    def hill_climbing(start_state, goal_state):
        current_state = start_state
        path = [start_state] 
        
        while True:
            neighbors = generate_neighbors(current_state)
            if not neighbors:
                break 

            next_state = min(neighbors, key=lambda state: manhattan_distance(state, goal_state))

            if manhattan_distance(next_state, goal_state) >= manhattan_distance(current_state, goal_state):
                break 

            current_state = next_state
            path.append(current_state) 
        
        return path if current_state == goal_state else None
    
    return hill_climbing(start_state, goal_state)

def SAHC(start_state, goal_state):

    def steepest_ascent_hill_climbing(start_state, goal_state):
        current_state = start_state
        path = [start_state]  
        
        while True:
            neighbors = generate_neighbors(current_state)
            if not neighbors:
                break  

            best_neighbor = min(neighbors, key=lambda state: manhattan_distance(state, goal_state))
            best_neighbor_distance = manhattan_distance(best_neighbor, goal_state)
            current_distance = manhattan_distance(current_state, goal_state)

            if best_neighbor_distance >= current_distance:
                break  

            current_state = best_neighbor
            path.append(current_state) 
        
        return path if current_state == goal_state else None
    
    return steepest_ascent_hill_climbing(start_state, goal_state)

def Stochastic(start_state, goal_state):

    def stochastic_hill_climbing(start_state, goal_state):
        current_state = start_state
        path = [start_state]  

        while True:
            neighbors = generate_neighbors(current_state)
            if not neighbors:
                break  
            
            better_neighbors = [state for state in neighbors if manhattan_distance(state, goal_state) < manhattan_distance(current_state, goal_state)]

            if not better_neighbors:
                break  
            
            current_state = random.choice(better_neighbors)
            path.append(current_state)

        return path if current_state == goal_state else None

    return stochastic_hill_climbing(start_state, goal_state)

def SA(start_state, goal_state, initial_temp=100, cooling_rate=0.99, min_temp=0.1):

    current_state = start_state
    current_temp = initial_temp
    path = [start_state]

    while current_temp > min_temp:
        neighbors = generate_neighbors(current_state)
        if not neighbors:
            break  

        next_state = random.choice(neighbors)

        current_energy = manhattan_distance(current_state, goal_state)
        next_energy = manhattan_distance(next_state, goal_state)
        delta_energy = next_energy - current_energy

        # Acceptance probability 
        if delta_energy < 0 or random.uniform(0, 1) < math.exp(-delta_energy / current_temp):
            current_state = next_state
            path.append(current_state)

        current_temp *= cooling_rate
        
        if current_state == goal_state:
            return path

    return path if current_state == goal_state else None

def BS(start_state, goal_state, beam_width=2):
    
    frontier = [(manhattan_distance(start_state, goal_state), start_state, [])]
    visited = set()
    visited.add(state_to_tuple(start_state))

    while frontier:
        new_frontier = []
        
        for _, current_state, path in frontier:
            if current_state == goal_state:
                return [start_state] + path
            
            for neighbor in generate_neighbors(current_state):
                neighbor_tuple = state_to_tuple(neighbor)
                if neighbor_tuple not in visited:
                    visited.add(neighbor_tuple)
                    heappush(new_frontier, (manhattan_distance(neighbor, goal_state), neighbor, path + [neighbor]))

        frontier = [heappop(new_frontier) for _ in range(min(beam_width, len(new_frontier)))]
    
    return None

def GEN(start_state, goal_state):
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
        return sum(
            1 for i in range(3) for j in range(3)
            if state[i][j] != 0 and state[i][j] == goal_state[i][j]
        )

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
                    print(f"✅ Tìm thấy lời giải ở thế hệ {gen}")
                    return path_states

            scored.sort(key=lambda x: x[0])
            best_score = scored[0][0]
            print(f"Thế hệ {gen}, tốt nhất: {best_score}")

            # Elitism: giữ lại top cá thể
            next_gen = [scored[i][1] for i in range(min(beam_width, len(scored)))]

            while len(next_gen) < pop_size:
                p1 = random.choice(scored[:beam_width])[1]
                p2 = random.choice(scored[:beam_width])[1]
                child = crossover(p1, p2)
                child = mutate(child)
                next_gen.append(child)

            population = next_gen

        print("❌ Không tìm thấy lời giải sau nhiều thế hệ.")
        return None

    return GA(start_state, goal_state)

#====================================================================================#
