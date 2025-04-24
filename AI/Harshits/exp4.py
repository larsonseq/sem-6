from collections import deque

# DFS implementation
def dfs(graph, start):
    visited = []  # List instead of set to maintain order
    stack = [start]  # Stack holds nodes
    traversal = []  # To keep track of the traversal order

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)  # Maintain order of visited nodes
            traversal.append(node)
            print(f"DFS - Current Node: {node}, Closed Nodes: {visited}")

            # Add neighbors to stack (reverse to maintain order)
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)

    print(f"DFS - Complete Traversal: {traversal}")
    return traversal


# BFS implementation
def bfs(graph, start):
    visited = []  # List instead of set to maintain order
    queue = deque([start])  # Queue holds nodes
    traversal = []  # To keep track of the traversal order

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)  # Maintain order of visited nodes
            traversal.append(node)
            print(f"BFS - Current Node: {node}, Closed Nodes: {visited}")

            # Add neighbors to queue
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)

    print(f"BFS - Complete Traversal: {traversal}")
    return traversal


# Take input for the graph
def input_graph():
    graph = {}
    num_nodes = int(input("Enter the number of nodes: "))

    for _ in range(num_nodes):
        node = input("Enter node: ").strip()  # Remove extra spaces
        neighbors = input(f"Enter neighbors for {node}, separated by spaces: ").strip().split()
        neighbors = [neighbor.strip() for neighbor in neighbors]  # Ensure no spaces in names
        graph[node] = neighbors

    return graph


# Take input for the starting node
def get_start_node():
    start = input("Enter the starting node: ")
    return start


# Main function to execute
def main():
    graph = input_graph()
    start_node = get_start_node()

    print("\nDFS Traversal:")
    dfs(graph, start_node)

    print("\nBFS Traversal:")
    bfs(graph, start_node)


if __name__ == "__main__":
    main()
