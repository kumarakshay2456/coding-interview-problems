from collections import deque

def get_visited_component(source, graph, visited_nodes):
    queue = deque([source])
    while queue:
        node = queue.popleft()
        if node not in visited_nodes:
            visited_nodes.add(node)
            for neighbour in graph.get(node):
                queue.append(neighbour)
    return visited_nodes

def count_component(graph):
    component = 0
    visited_nodes = set()
    for node in graph:
        if node not in visited_nodes:
            get_visited_component(node, graph, visited_nodes)
            component += 1
    return component

graph = {
    0:[1],
    1:[0,2],
    2:[1],
    3:[4],
    4:[3],
    5:[]
}

print("Total components are", count_component(graph))
