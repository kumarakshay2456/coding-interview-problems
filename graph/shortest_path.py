""""
Have the function ShortestPath(strArr) take strArr, which will be an array of strings that models a non-looping graph (a directed or undirected graph with no cycles). The structure of the array is as follows:
	1.	The first element will be an integer N (as a string) representing the number of nodes in the graph.
	2.	The next N elements will be the names of the nodes. These can be simple names like "A", "B" or more complex names like "Main Street", "Brick Road", etc.
	3.	The remaining elements in the array will be connections between nodes, formatted as "Node1-Node2" (e.g., "A-B", "Brick Road-Main Street").

Your task is to return the shortest path (in terms of number of edges) from the first node in the node list to the last node in the node list.
	•	If there is no possible path, return "no path".
	•	If a path exists, return the path as a string of node names joined with dashes, like "A-B-D".

EX - strArr = ["4", "A", "B", "C", "D", "A-B", "B-D", "B-C", "C-D"]
Nodes: A, B, C, D
Edges: A-B, B-D, B-C, C-D
Start: A
End: D

output - "A-B-D"

"""
from collections import defaultdict, deque
def sortest_path(arr):
    n = int(arr[0])
    nodes = arr[1:n+1]  
    edges = arr[n+1:]
    graph = defaultdict(list)
    for i in edges:
        u, v = i.split('-')
        graph[u].append(v)
        graph[v].append(u)
    start = nodes[0]
    end = nodes[-1]

    queue = deque([[start]]) 
    visited = set()

    while queue:
        path = queue.popleft()
        print("path is", path)
        current = path[-1]

        if current == end:
            return "-".join(path)

        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    queue.append(path + [neighbor])

    return "no path"
arr = ["4", "A", "B", "C", "D", "A-B", "B-D", "B-C", "C-D"]
sortest_path(arr)

"""
Concept                   |          Description
1.    deque([[start]])          |          Stores full path (not just node), enabling immediate return when goal found
                          |
2.    path + [neighbor]         |         Creates a new path list for each BFS branch
3.    visited set               |        Prevents revisiting nodes, avoids infinite loops
4.    BFS vs DFS for shortest   |       BFS is preferred as it finds shortest path in unweighted graphs

"""