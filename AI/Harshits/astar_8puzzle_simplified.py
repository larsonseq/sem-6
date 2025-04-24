
import heapq
import time
from copy import deepcopy

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.heuristic = 0
        self.f_score = 0

    def __lt__(self, other):
        return self.f_score < other.f_score

def print_puzzle(state):
    for row in state:
        print("+---" * 3 + "+")
        print("| " + " | ".join(' ' if n == 0 else str(n) for n in row) + " |")
    print("+---" * 3 + "+")

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(node):
    moves = [('UP', -1, 0), ('DOWN', 1, 0), ('LEFT', 0, -1), ('RIGHT', 0, 1)]
    neighbors = []
    i, j = find_blank(node.state)
    for move, di, dj in moves:
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_state = deepcopy(node.state)
            new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
            neighbors.append(PuzzleNode(new_state, node, move, node.depth + 1))
    return neighbors

def manhattan_distance(state, goal):
    dist = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                for x in range(3):
                    for y in range(3):
                        if goal[x][y] == val:
                            dist += abs(x - i) + abs(y - j)
                            break
    return dist

def misplaced_tiles(state, goal):
    return sum(1 for i in range(3) for j in range(3) if state[i][j] and state[i][j] != goal[i][j])

def astar_search(start, goal, heuristic_name):
    heuristic_func = manhattan_distance if heuristic_name == "manhattan" else misplaced_tiles
    start_node = PuzzleNode(start)
    start_node.heuristic = heuristic_func(start, goal)
    start_node.f_score = start_node.depth + start_node.heuristic

    open_set = [start_node]
    closed_set = set()
    heapq.heapify(open_set)

    while open_set:
        node = heapq.heappop(open_set)
        if node.state == goal:
            return reconstruct_path(node), len(closed_set)
        closed_set.add(str(node.state))
        for neighbor in get_neighbors(node):
            if str(neighbor.state) in closed_set:
                continue
            neighbor.heuristic = heuristic_func(neighbor.state, goal)
            neighbor.f_score = neighbor.depth + neighbor.heuristic
            heapq.heappush(open_set, neighbor)
    return None, len(closed_set)

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.state, node.move, node.depth, node.heuristic))
        node = node.parent
    return path[::-1]

def is_solvable(state):
    flat = [n for row in state for n in row if n != 0]
    inversions = sum(1 for i in range(len(flat)) for j in range(i + 1, len(flat)) if flat[i] > flat[j])
    return inversions % 2 == 0

def main():
    start = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    heuristic = "manhattan"

    if is_solvable(start) != is_solvable(goal):
        print("This puzzle configuration is not solvable.")
        return

    print("Initial State:")
    print_puzzle(start)
    print("Goal State:")
    print_puzzle(goal)

    start_time = time.time()
    path, steps = astar_search(start, goal, heuristic)
    end_time = time.time()

    if path:
        print(f"Solution found in {steps} steps, time: {end_time - start_time:.2f}s")
        for i, (state, move, depth, h) in enumerate(path):
            print(f"Step {i}: {move if move else 'Start'} (g={depth}, h={h}, f={depth+h})")
            print_puzzle(state)
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
