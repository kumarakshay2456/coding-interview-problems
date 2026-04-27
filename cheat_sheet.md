# DSA Interview Cheat Sheet

Quick reference for complexities, patterns, and Python built-ins.
Keep this open during mock interviews.

---

## Data Structure Complexities

| Structure | Access | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Dynamic Array (list) | O(1) | O(n) | O(1) amort. | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Hash Map | O(1) avg | O(1) avg | O(1) avg | O(1) avg | O(n) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| BST (skewed) | O(n) | O(n) | O(n) | O(n) | O(n) |
| Heap (min/max) | O(1) top | O(n) | O(log n) | O(log n) | O(n) |
| Trie | — | O(L) | O(L) | O(L) | O(N*L) |

---

## Sorting Algorithm Complexities

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| Python `sort()` | — | O(n log n) | O(n log n) | O(n) | Yes (Timsort) |

---

## Graph Algorithm Complexities

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| BFS | O(V+E) | O(V) | Shortest path (unweighted), level-order |
| DFS | O(V+E) | O(V) | Connectivity, cycle detection, topological sort |
| Dijkstra | O((V+E) log V) | O(V) | Shortest path (non-negative weights) |
| Bellman-Ford | O(V*E) | O(V) | Shortest path (negative weights) |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest path |
| Kruskal's MST | O(E log E) | O(V) | Minimum spanning tree |
| Prim's MST | O(E log V) | O(V) | Minimum spanning tree (dense graphs) |
| Topological Sort | O(V+E) | O(V) | DAG ordering (Kahn's BFS or DFS) |
| Union-Find | O(α(n)) ≈ O(1) | O(n) | Connectivity, cycle detection, MST |

---

## Pattern Recognition Quick Guide

| If the problem says... | Use this pattern |
|------------------------|-----------------|
| Contiguous subarray/substring with condition | Sliding Window |
| 2D grid, islands, flood fill | Matrix Traversal (BFS/DFS) |
| Sorted array, pair with target sum | Two Pointers |
| Linked list cycle, find middle | Fast & Slow Pointers |
| Overlapping intervals, meeting rooms | Merge Intervals |
| Array with numbers in range [1..n] | Cyclic Sort |
| Reverse part of a linked list | In-place LL Reversal |
| Level order, shortest path | BFS |
| All paths, exhaustive search | DFS / Backtracking |
| Median, largest/smallest of two halves | Two Heaps |
| Permutations, combinations, subsets | Subsets / Backtracking |
| Sorted but rotated, find boundary | Modified Binary Search |
| Find single/missing using XOR | Bitwise XOR |
| Top/bottom K elements | Heap (Top K) |
| Merge K sorted lists | K-way Merge (Heap) |
| Build order, prerequisites | Topological Sort |
| Max/min with one element per row | 0/1 Knapsack |
| Sequence depends on previous 1-2 steps | Fibonacci DP |
| Palindrome optimization | Palindromic DP |
| Compare two strings optimally | LCS DP |
| Next greater/smaller element | Monotonic Stack |
| Cache with fast eviction | LRU (HashMap + DLL) |
| String prefix matching, autocomplete | Trie |
| Graph connectivity, no extra space | Union-Find |

---

## Python Built-ins Cheat Sheet

```python
# Heap (min-heap by default)
import heapq
h = []
heapq.heappush(h, val)
heapq.heappop(h)           # removes and returns smallest
heapq.heapify(list)        # O(n) in-place
heapq.nlargest(k, iterable)
heapq.nsmallest(k, iterable)
# Max-heap: negate values → push(-val), then -heappop(h)

# Deque (O(1) both ends)
from collections import deque
d = deque()
d.append(x)        # right
d.appendleft(x)    # left
d.pop()            # right
d.popleft()        # left

# Counter
from collections import Counter
c = Counter(list)
c.most_common(k)   # top k (val, count) pairs

# DefaultDict
from collections import defaultdict
d = defaultdict(list)   # d[missing_key] → []
d = defaultdict(int)    # d[missing_key] → 0

# OrderedDict (LRU Cache)
from collections import OrderedDict
od = OrderedDict()
od.move_to_end(key)           # move to right (most recent)
od.move_to_end(key, last=False)  # move to left (oldest)
od.popitem(last=False)        # remove leftmost

# Binary Search
import bisect
bisect.bisect_left(a, x)   # leftmost position to insert x
bisect.bisect_right(a, x)  # rightmost position to insert x
bisect.insort(a, x)        # insert x maintaining sort order

# Sorting
sorted(lst, key=lambda x: x[1])          # by second element
sorted(lst, key=lambda x: (x[1], x[0])) # multi-key sort
lst.sort(reverse=True)
```

---

## Tree Traversal Templates

```python
# Inorder (Left → Root → Right) — gives sorted order for BST
def inorder(root):
    if not root: return
    inorder(root.left)
    visit(root)
    inorder(root.right)

# Preorder (Root → Left → Right) — good for serialization
def preorder(root):
    if not root: return
    visit(root)
    preorder(root.left)
    preorder(root.right)

# Postorder (Left → Right → Root) — good for deletion
def postorder(root):
    if not root: return
    postorder(root.left)
    postorder(root.right)
    visit(root)

# Level Order (BFS)
from collections import deque
def level_order(root):
    if not root: return
    q = deque([root])
    while q:
        for _ in range(len(q)):
            node = q.popleft()
            visit(node)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
```

---

## Graph Templates

```python
# BFS
from collections import deque
def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

# DFS (recursive)
def dfs(graph, node, visited=None):
    if visited is None: visited = set()
    visited.add(node)
    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs(graph, neighbour, visited)

# Topological Sort (Kahn's BFS)
from collections import deque, defaultdict
def topo_sort(n, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * n
    for u, v in prerequisites:
        graph[v].append(u)
        in_degree[u] += 1
    queue = deque(i for i in range(n) if in_degree[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            in_degree[nei] -= 1
            if in_degree[nei] == 0:
                queue.append(nei)
    return order if len(order) == n else []   # empty = cycle
```

---

## Binary Search Templates

```python
# Standard: find exact target
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target: return mid
        elif nums[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1

# Left boundary (first position where nums[i] >= target)
def lower_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target: lo = mid + 1
        else: hi = mid
    return lo

# Search on answer (minimise x such that condition(x) is True)
def binary_search_on_answer(lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        if condition(mid): hi = mid
        else: lo = mid + 1
    return lo
```

---

## Sliding Window Template

```python
def sliding_window(nums, k):
    left = 0
    window_state = ...   # sum, count, set, etc.
    result = ...

    for right in range(len(nums)):
        # expand window: add nums[right]
        window_state += nums[right]

        # shrink window when invalid
        while window_is_invalid(window_state):
            window_state -= nums[left]
            left += 1

        # update result (window is now valid)
        result = max(result, right - left + 1)

    return result
```

---

## Backtracking Template

```python
def backtrack(state, choices):
    if is_solution(state):
        result.append(state[:])
        return
    for choice in choices:
        if is_valid(choice, state):
            state.append(choice)
            backtrack(state, next_choices(choice))
            state.pop()   # undo choice
```

---

## Complexity — Big O Reference

| n | Max operations affordable | Algorithm class |
|---|--------------------------|----------------|
| ≤ 10 | 10! = 3.6M | O(n!) — permutations |
| ≤ 25 | 2^25 = 33M | O(2^n) — subsets |
| ≤ 300 | 300³ = 27M | O(n³) — 3D DP |
| ≤ 5000 | 5000² = 25M | O(n²) — 2D DP, bubble sort |
| ≤ 10^6 | 20M ops | O(n log n) — sorting, heap |
| ≤ 10^8 | 10^8 ops | O(n) — single pass |
| Any | 1 op | O(1) — hash lookup |

---

## Interview Day Checklist

- [ ] Clarify: input size, edge cases (empty, single element, negatives, duplicates)
- [ ] State the approach + complexity before coding
- [ ] Write clean variable names — no `a`, `b`, `x` for pointers
- [ ] Walk through a small example by hand
- [ ] Check edge cases: empty input, n=1, all same elements
- [ ] Mention space optimisation if asked (e.g., 2D DP → 1D)
- [ ] Test your code with the example, then a tricky case
