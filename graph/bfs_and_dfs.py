from collections import deque
class Graph:
    def __init__(self):
        self.adj = {}
    
    def add_edge(self, u,v):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)

    def print_grpah(self):
        for node in self.adj:
            print(f"{node} --> {self.adj[node]}")
    
    def bfs(self, start):
        visited_node = []
        queue = deque()
        queue.append(start)
        while queue:
            node = queue.popleft()
            if node not in visited_node:
                # print(node, end=" ")
                visited_node.append(node)
                for neighbor in self.adj.get(node, []):
                    queue.append(neighbor)
        print("BFS node is", visited_node)
    
    def dfs(self, start):
        visited_node = []
        stack = []
        stack.append(start)
        while stack:
            node = stack.pop()
            if node not in visited_node:
                # print(node, end=" ")
                visited_node.append(node)
                stack.extend(reversed(self.adj.get(node, [])))
        print("DFS IS", ' '.join(str(node) for node in visited_node))
            
    

"""
Time and Space - T(n) = O(v+E)
Space - T(n) = O(V)

Method         Your Time Complexity      Optimal Time     Space Complexity
bfs()             O(V * V + E)             O(V + E)            O(V)
dfs()             O(V * v + E)             O(V + E)            O(V)

To get actual O(V + E) time, use a set for visited_node:
visited_node = set()
if node not in visited_node:
    visited_node.add(node)
Then store the final visited order separately if needed:
result = []
...
    result.append(node)
"""

g = Graph()
g.add_edge(1,2)
g.add_edge(1,6)
g.add_edge(2,1)
g.add_edge(2,4)
g.add_edge(2,3)
g.add_edge(4,2)
g.add_edge(4,5)
g.add_edge(5,4)
g.add_edge(5,8)
g.add_edge(8,7)
g.add_edge(8,5)
g.add_edge(7,6)
g.add_edge(7,8)
g.add_edge(6,1)
g.add_edge(6,7)
g.add_edge(6,9)
g.print_grpah()
g.bfs(1)
g.dfs(1)


