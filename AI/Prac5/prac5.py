import heapq
import copy
import time

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = 0
        self.heuristic = 0
        self.f_score = 0

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(str(self.state))

def print_puzzle(state):
    """Print the 8-puzzle state in a readable format"""
    for i in range(3):
        print("+---+---+---+")
        print("|", end=" ")
        for j in range(3):
            if state[i][j] == 0:
                print(" ", end=" | ")
            else:
                print(state[i][j], end=" | ")
        print()
    print("+---+---+---+")

def find_blank(state):
    """Find the coordinates of the blank (0) in the puzzle"""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return -1, -1

def get_neighbors(node):
    """Generate all possible moves from current state"""
    neighbors = []
    i, j = find_blank(node.state)
    possible_moves = [('UP', -1, 0), ('DOWN', 1, 0), ('LEFT', 0, -1), ('RIGHT', 0, 1)]
    
    for move_name, di, dj in possible_moves:
        new_i, new_j = i + di, j + dj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = copy.deepcopy(node.state)
            new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
            new_node = PuzzleNode(new_state, node, move_name, node.depth + 1)
            neighbors.append(new_node)
    
    return neighbors

def manhattan_distance(state, goal):
    """Calculate Manhattan distance heuristic"""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                # Find where this tile should be in the goal state
                for gi in range(3):
                    for gj in range(3):
                        if goal[gi][gj] == state[i][j]:
                            distance += abs(i - gi) + abs(j - gj)
                            break
    return distance

def misplaced_tiles(state, goal):
    """Calculate number of misplaced tiles heuristic"""
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count += 1
    return count

def astar_search(initial_state, goal_state, heuristic_func):
    """A* search algorithm for 8-puzzle"""
    initial_node = PuzzleNode(initial_state)
    
    if heuristic_func == "manhattan":
        initial_node.heuristic = manhattan_distance(initial_state, goal_state)
    else:
        initial_node.heuristic = misplaced_tiles(initial_state, goal_state)
    
    initial_node.f_score = initial_node.depth + initial_node.heuristic
    
    open_set = [initial_node]
    heapq.heapify(open_set)
    closed_set = set()
    
    steps = 0
    max_steps = 100000  # Limit to prevent infinite loops
    
    while open_set and steps < max_steps:
        steps += 1
        current_node = heapq.heappop(open_set)
        
        # Check if goal reached
        if current_node.state == goal_state:
            return reconstruct_path(current_node), steps
        
        # Add to closed set
        closed_set.add(hash(str(current_node.state)))
        
        # Generate neighbors
        for neighbor in get_neighbors(current_node):
            if hash(str(neighbor.state)) in closed_set:
                continue
            
            if heuristic_func == "manhattan":
                neighbor.heuristic = manhattan_distance(neighbor.state, goal_state)
            else:
                neighbor.heuristic = misplaced_tiles(neighbor.state, goal_state)
            
            neighbor.f_score = neighbor.depth + neighbor.heuristic
            
            # Check if this node is already in open_set with worse score
            skip = False
            for i, node in enumerate(open_set):
                if node.state == neighbor.state and node.f_score <= neighbor.f_score:
                    skip = True
                    break
            
            if not skip:
                heapq.heappush(open_set, neighbor)
    
    return None, steps

def reconstruct_path(node):
    """Reconstruct the path from initial state to goal"""
    path = []
    while node:
        path.append((node.state, node.move))
        node = node.parent
    return path[::-1]  # Reverse to get from initial to goal

def input_puzzle_state(prompt):
    """Get puzzle state input from user"""
    print(prompt)
    print("Enter the puzzle as a single line of 9 numbers, where 0 represents the blank space.")
    print("For example: 1 2 3 4 0 5 6 7 8")
    
    while True:
        try:
            # Get input and convert to list of integers
            input_str = input("> ")
            numbers = [int(x) for x in input_str.strip().split()]
            
            # Verify we have exactly 9 numbers from 0-8
            if len(numbers) != 9:
                print("Please enter exactly 9 numbers.")
                continue
            
            # Verify each number appears exactly once
            if sorted(numbers) != list(range(9)):
                print("Please use each number from 0-8 exactly once.")
                continue
            
            # Convert flat list to 3x3 grid
            state = [numbers[i:i+3] for i in range(0, 9, 3)]
            return state
            
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")

def is_solvable(state):
    """Check if the puzzle is solvable"""
    """
    An inversion is a pair of tiles (a, b) such that a appears before b, but a > b. The blank (0) is ignored.
    So, for each number, it checks how many smaller numbers come after it in the list.
    If the number of inversions is even, the puzzle is solvable.
    If odd, it's unsolvable.
    """
    # Convert to 1D array for easier processing
    flat = [val for row in state for val in row]
    
    # Count inversions
    inversions = 0
    for i in range(len(flat)):
        if flat[i] == 0:
            continue
        for j in range(i + 1, len(flat)):
            if flat[j] == 0:
                continue
            if flat[i] > flat[j]:
                inversions += 1
    
    return inversions % 2 == 0

def main():
    print("\n===== 8-PUZZLE SOLVER USING A* SEARCH =====\n")
    
    # Input states
    initial_state = input_puzzle_state("Enter the INITIAL state of the puzzle:")
    print("\nInitial state:")
    print_puzzle(initial_state)
    
    goal_state = input_puzzle_state("Enter the GOAL state of the puzzle:")
    print("\nGoal state:")
    print_puzzle(goal_state)
    
    # Check if the puzzle is solvable
    if not is_solvable(initial_state) == is_solvable(goal_state):
        print("\nThe given puzzle is not solvable to reach the goal state.")
        return
    
    # Select heuristic
    print("\nSelect heuristic function:")
    print("1. Manhattan distance")
    print("2. Misplaced tiles")
    
    heuristic_choice = input("Enter choice (1 or 2): ")
    heuristic = "manhattan" if heuristic_choice == "1" else "misplaced"
    
    print(f"\nUsing {heuristic} heuristic to solve the puzzle...")
    start_time = time.time()
    
    # Solve the puzzle
    path, steps = astar_search(initial_state, goal_state, heuristic)
    
    end_time = time.time()
    
    if path:
        print(f"\nSolution found in {steps} steps!")
        print(f"Time taken: {end_time - start_time:.4f} seconds")
        print(f"Solution length: {len(path) - 1} moves\n")
        
        print("===== SOLUTION PATH =====")
        for i, (state, move) in enumerate(path):
            print(f"\nStep {i}: {move if move else 'Initial State'}")
            print_puzzle(state)
            if i < len(path) - 1:
                print("↓")
    else:
        print("\nNo solution found within the step limit.")

if __name__ == "__main__":
    main()

