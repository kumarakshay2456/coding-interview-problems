from collections import defaultdict, deque

class Graph:
    def __init__(self) -> None:
        self.graph = defaultdict(list)

    def add_node(self, u,v):
        self.graph[u].append(v)
    
    def print_graph(self):
        for key, value in self.graph.items():

            print(f"{key} --- {','.join(map(str, value))}")    
    def get_shortet_path(self, start, end):
        queue = deque([(start, [start])])
        visited = set()
        sortest_data = [] 
        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.get(node, []):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        return None

g = Graph()
g.add_node(1, 2)
g.add_node(1, 5)

g.add_node(2, 1)
g.add_node(2, 3)
g.add_node(2, 6)

g.add_node(3, 2)
g.add_node(3, 4)
g.add_node(3, 7)

g.add_node(4, 3)
g.add_node(4, 8)

g.add_node(5, 1)
g.add_node(5, 6)

g.add_node(6, 2)
g.add_node(6, 5)
g.add_node(6, 7)
g.add_node(6, 9)

g.add_node(7, 3)
g.add_node(7, 6)
g.add_node(7, 8)

g.add_node(8, 4)
g.add_node(8, 7)
g.add_node(8, 10)

g.add_node(9, 6)
g.add_node(9, 10)

g.add_node(10, 8)
g.add_node(10, 9)
start = 1
end = 10
print(f"Sortest path from {start} and {end} is -> {g.get_shortet_path(start, end)}")





