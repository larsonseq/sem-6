from collections import deque


def dfs(graph, start):
    stack = [start]
    visited = []
    traversal = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            traversal.append(node)
            print(f"DFS - Current Node: {node}, Closed Nodes: {visited}")

            for neighbours in reversed(graph[node]):
                if neighbours not in visited:
                    stack.append(neighbours)


def bfs(graph, start_node):
    queue = deque([start_node])
    traversal = []
    visited = []

    while queue:
        node = queue.popleft()

        if node not in visited:
            visited.append(node)
            traversal.append(node)
            print(f"BFS - Current Node: {node}, Closed Nodes: {traversal}")

            for neighbors in graph[node]:
                if neighbors not in visited:
                    queue.append(neighbors)


def input_graph():
    graph = {}

    while True:
        print("Enter Nodes : \n(Enter 'end' to stop)")
        node = input().strip()
        if node.lower() == 'end':
            return graph
        neighbours = input(f"Enter Neighbours of {node} seperated by space: ").strip().split()
        graph[node] = neighbours 


def input_start_node(graph):
    while True:
        start_node = input(f"Enter Start Node: ")
        if start_node not in graph:
            print("Start Node not in Graph!!\nTryAgain")
            continue 
        return start_node 


def main():
    graph = input_graph()
    start_node = input_start_node(graph)

    for i in graph:
        print(f"Node: {i}\tNeigh: {graph[i]}")

    dfs(graph, start_node)

    bfs(graph, start_node)


if __name__ == "__main__":
    main()