from collections import deque
import copy
from queue import PriorityQueue
import random
import math

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def BFS(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
        
    visited.add(state_to_tuple(start_state))
    while queue:
        current, path = queue.popleft()
        
        if current == goal_state:
            return [start_state] + path
        
        # Find 0
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

start = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]

goal = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

result = BFS(start, goal)

if result:
    print("Tìm thấy lời giải với độ dài:", len(result) - 1)
    for step in result:
        for row in step:
            print(row)
        print("---")
else:
    print("Không tìm thấy lời giải.")
