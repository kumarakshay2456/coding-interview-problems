"""
Union-Find (Disjoint Set Union — DSU)

With path compression + union by rank:
  find:  O(α(n)) ≈ O(1) amortised
  union: O(α(n)) ≈ O(1) amortised

Covers:
  1. Core DSU implementation
  2. Number of Connected Components in Undirected Graph
  3. Detect Cycle in Undirected Graph
  4. Redundant Connection (LeetCode 684)
  5. Minimum Spanning Tree — Kruskal's Algorithm
"""


# ── 1. Core DSU ───────────────────────────────────────────────────────────────

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False   # already in the same set
        # union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


# ── 2. Number of Connected Components ─────────────────────────────────────────
# Given n nodes and a list of edges, return the number of connected components.
# Time: O(E * α(n))  Space: O(n)

def count_components(n: int, edges: list[list[int]]) -> int:
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.components


# ── 3. Detect Cycle in Undirected Graph ───────────────────────────────────────
# If union returns False, the two nodes are already connected → adding this
# edge would create a cycle.
# Time: O(E * α(n))  Space: O(n)

def has_cycle(n: int, edges: list[list[int]]) -> bool:
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return True
    return False


# ── 4. Redundant Connection ───────────────────────────────────────────────────
# Return the last edge that creates a cycle.
# Time: O(E * α(n))  Space: O(n)

def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    uf = UnionFind(len(edges) + 1)
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    return []


# ── 5. Kruskal's Minimum Spanning Tree ────────────────────────────────────────
# edges = [(weight, u, v), ...]
# Returns total MST weight and the edges included.
# Time: O(E log E)  Space: O(n)

def kruskal_mst(n: int, edges: list[tuple[int, int, int]]):
    uf = UnionFind(n)
    mst_edges = []
    total_weight = 0
    for weight, u, v in sorted(edges):
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            if len(mst_edges) == n - 1:
                break
    return total_weight, mst_edges


# ── Tests ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("── Connected Components ──")
    print(count_components(5, [[0,1],[1,2],[3,4]]))   # 2
    print(count_components(5, [[0,1],[1,2],[2,3],[3,4]]))  # 1

    print("\n── Cycle Detection ──")
    print(has_cycle(3, [[0,1],[1,2],[2,0]]))   # True
    print(has_cycle(3, [[0,1],[1,2]]))          # False

    print("\n── Redundant Connection ──")
    print(find_redundant_connection([[1,2],[1,3],[2,3]]))   # [2,3]
    print(find_redundant_connection([[1,2],[2,3],[3,4],[1,4],[1,5]]))  # [1,4]

    print("\n── Kruskal's MST ──")
    edges = [(1,0,1),(4,0,2),(3,1,2),(2,1,3),(5,2,3)]
    weight, mst = kruskal_mst(4, edges)
    print(f"MST weight: {weight}, edges: {mst}")   # weight: 6
