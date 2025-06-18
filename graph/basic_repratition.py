class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)

    def print_graph(self):
        for node in self.adj:
            print(f"{node} --> {self.adj[node]}")

g = Graph()
g.add_edge('A','B')
g.add_edge('A','C')
g.add_edge('B','D')
g.print_graph()