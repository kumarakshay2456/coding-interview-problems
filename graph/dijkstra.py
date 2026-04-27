"""
Dijkstra's Shortest Path Algorithm

Works on weighted graphs with non-negative edge weights.
Uses a min-heap (priority queue) to always expand the cheapest node next.

Time:  O((V + E) log V)
Space: O(V + E)

Covers:
  1. Single-source shortest distances
  2. Reconstruct the actual path
  3. Network Delay Time (LeetCode 743)
  4. Cheapest Flights Within K Stops (modified Dijkstra / Bellman-Ford)
  5. Path with Minimum Effort (LeetCode 1631)
"""

import heapq
from collections import defaultdict


# ── 1. Single-Source Shortest Distances ───────────────────────────────────────
# graph: adjacency list {u: [(v, weight), ...]}
# Returns dist[] where dist[v] = shortest distance from src to v.
# dist[v] = infinity if unreachable.

def dijkstra(graph: dict[int, list[tuple[int, int]]], src: int, n: int) -> list[float]:
    dist = [float("inf")] * n
    dist[src] = 0
    min_heap = [(0, src)]   # (distance, node)

    while min_heap:
        d, u = heapq.heappop(min_heap)
        if d > dist[u]:
            continue   # stale entry
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(min_heap, (dist[v], v))

    return dist


# ── 2. Reconstruct Shortest Path ──────────────────────────────────────────────

def dijkstra_with_path(
    graph: dict[int, list[tuple[int, int]]], src: int, dst: int, n: int
) -> tuple[float, list[int]]:
    dist = [float("inf")] * n
    prev = [-1] * n
    dist[src] = 0
    min_heap = [(0, src)]

    while min_heap:
        d, u = heapq.heappop(min_heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(min_heap, (dist[v], v))

    if dist[dst] == float("inf"):
        return float("inf"), []

    path = []
    node = dst
    while node != -1:
        path.append(node)
        node = prev[node]
    return dist[dst], path[::-1]


# ── 3. Network Delay Time ─────────────────────────────────────────────────────
# Given n nodes, edges = [[u, v, w]], and a source k,
# return the time for all nodes to receive the signal, or -1 if impossible.
# Time: O((V+E) log V)  Space: O(V+E)

def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = dijkstra(graph, k, n + 1)   # nodes are 1-indexed
    max_dist = max(dist[1:])            # skip dist[0] (unused)
    return -1 if max_dist == float("inf") else max_dist


# ── 4. Path with Minimum Effort ───────────────────────────────────────────────
# Grid problem: effort = max absolute difference along a path.
# Minimise the maximum effort from top-left to bottom-right.
# Time: O(m*n * log(m*n))  Space: O(m*n)

def minimum_effort_path(heights: list[list[int]]) -> int:
    rows, cols = len(heights), len(heights[0])
    effort = [[float("inf")] * cols for _ in range(rows)]
    effort[0][0] = 0
    min_heap = [(0, 0, 0)]   # (max_effort_so_far, row, col)

    while min_heap:
        e, r, c = heapq.heappop(min_heap)
        if e > effort[r][c]:
            continue
        if r == rows - 1 and c == cols - 1:
            return e
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_effort = max(e, abs(heights[nr][nc] - heights[r][c]))
                if new_effort < effort[nr][nc]:
                    effort[nr][nc] = new_effort
                    heapq.heappush(min_heap, (new_effort, nr, nc))

    return 0


# ── Tests ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("── Shortest Distances ──")
    g = defaultdict(list)
    edges = [(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5)]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))
    print(dijkstra(g, 0, 4))   # [0, 3, 1, 4]

    print("\n── Shortest Path ──")
    dist, path = dijkstra_with_path(g, 0, 3, 4)
    print(f"Distance: {dist}, Path: {path}")   # Distance: 4, Path: [0, 2, 1, 3]

    print("\n── Network Delay Time ──")
    times = [[2,1,1],[2,3,1],[3,4,1]]
    print(network_delay_time(times, 4, 2))   # 2

    print("\n── Minimum Effort Path ──")
    heights = [[1,2,2],[3,8,2],[5,3,5]]
    print(minimum_effort_path(heights))   # 2
