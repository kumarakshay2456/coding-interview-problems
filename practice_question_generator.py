"""
Random Practice Question Generator
Generates practice problems from the 20 DSA patterns for daily interview prep.
Usage:
    python practice_question_generator.py
    python practice_question_generator.py --pattern "Sliding Window"
    python practice_question_generator.py --difficulty easy
    python practice_question_generator.py --count 5
    python practice_question_generator.py --list-patterns
"""

import random
import argparse
import textwrap
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Problem:
    name: str
    pattern: str
    difficulty: str        # easy | medium | hard
    time_complexity: str
    space_complexity: str
    hint: str
    approach: str
    tags: list[str] = field(default_factory=list)


PROBLEMS: list[Problem] = [
    # ── Pattern 1: Sliding Window ──────────────────────────────────────────
    Problem(
        name="Maximum Sum Subarray of Size K",
        pattern="Sliding Window",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Maintain a running sum. When window exceeds K, subtract the leftmost element.",
        approach="Add element on right, remove element on left when window size > K.",
        tags=["array", "sliding window"],
    ),
    Problem(
        name="Longest Substring Without Repeating Characters",
        pattern="Sliding Window",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(min(m,n))",
        hint="Use a HashSet to track characters in the window. Shrink from left when a repeat is found.",
        approach="Expand right pointer; when duplicate found, move left pointer past the previous occurrence.",
        tags=["string", "hash map", "sliding window"],
    ),
    Problem(
        name="Minimum Window Substring",
        pattern="Sliding Window",
        difficulty="hard",
        time_complexity="O(n)",
        space_complexity="O(k)",
        hint="Use two frequency maps — one for target, one for current window. Track 'formed' count.",
        approach="Expand right until window is valid, then shrink left to minimize. Record minimum.",
        tags=["string", "hash map", "sliding window"],
    ),
    Problem(
        name="Fruit Into Baskets",
        pattern="Sliding Window",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="You can hold at most 2 types of fruit. Keep a count map for the window.",
        approach="Expand right; if distinct types > 2, shrink from left until valid.",
        tags=["array", "hash map", "sliding window"],
    ),
    Problem(
        name="Longest Repeating Character Replacement",
        pattern="Sliding Window",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Track max frequency char in window. Window is valid if size - max_freq <= k.",
        approach="Expand window. If replacements needed > k, shrink left by 1.",
        tags=["string", "sliding window"],
    ),
    Problem(
        name="Find All Anagrams in a String",
        pattern="Sliding Window",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(k)",
        hint="Use a fixed-size window equal to the pattern length and compare frequency maps.",
        approach="Slide a window of len(p); compare char counts with pattern counts.",
        tags=["string", "hash map", "sliding window"],
    ),
    Problem(
        name="Subarray Sum Equals K",
        pattern="Sliding Window",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(n)",
        hint="Prefix sum + hash map. Look for prefix_sum - k in seen sums.",
        approach="Running sum. At each step check if (sum - k) is in prefix_sum map.",
        tags=["array", "prefix sum", "hash map"],
    ),

    # ── Pattern 2: Islands / Matrix Traversal ──────────────────────────────
    Problem(
        name="Number of Islands",
        pattern="Islands / Matrix Traversal",
        difficulty="medium",
        time_complexity="O(m*n)",
        space_complexity="O(m*n)",
        hint="DFS or BFS from each unvisited land cell, marking visited cells.",
        approach="Iterate grid. When '1' found, DFS to mark all connected '1's as visited, increment count.",
        tags=["matrix", "dfs", "bfs", "graph"],
    ),
    Problem(
        name="Flood Fill",
        pattern="Islands / Matrix Traversal",
        difficulty="easy",
        time_complexity="O(m*n)",
        space_complexity="O(m*n)",
        hint="BFS/DFS from source pixel, replacing old color with new color.",
        approach="If source color == new color, return. DFS to all 4 neighbors with old color.",
        tags=["matrix", "dfs", "bfs"],
    ),
    Problem(
        name="Word Search",
        pattern="Islands / Matrix Traversal",
        difficulty="medium",
        time_complexity="O(m*n*4^L)",
        space_complexity="O(L)",
        hint="DFS + backtracking. Mark cell as visited temporarily during path.",
        approach="For each cell, DFS in 4 directions matching word characters. Unmark on backtrack.",
        tags=["matrix", "dfs", "backtracking"],
    ),
    Problem(
        name="Unique Paths",
        pattern="Islands / Matrix Traversal",
        difficulty="medium",
        time_complexity="O(m*n)",
        space_complexity="O(m*n)",
        hint="DP grid: paths[i][j] = paths[i-1][j] + paths[i][j-1].",
        approach="Base case: first row and column = 1. Fill rest with sum from top and left.",
        tags=["matrix", "dp"],
    ),

    # ── Pattern 3: Two Pointers ────────────────────────────────────────────
    Problem(
        name="Container With Most Water",
        pattern="Two Pointers",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Start pointers at both ends. Move the shorter height inward.",
        approach="Area = min(h[l], h[r]) * (r - l). Move pointer with smaller height.",
        tags=["array", "two pointers", "greedy"],
    ),
    Problem(
        name="Trapping Rain Water",
        pattern="Two Pointers",
        difficulty="hard",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Track left_max and right_max. Water at i = min(left_max, right_max) - height[i].",
        approach="Two pointers from ends. Process side with smaller max; it determines water level.",
        tags=["array", "two pointers"],
    ),
    Problem(
        name="3Sum",
        pattern="Two Pointers",
        difficulty="medium",
        time_complexity="O(n²)",
        space_complexity="O(1)",
        hint="Sort first. Fix one element, use two pointers for the remaining pair.",
        approach="Sort. For each i, two-pointer search in i+1..n-1 for pairs summing to -nums[i].",
        tags=["array", "two pointers", "sorting"],
    ),
    Problem(
        name="Sort Colors (0, 1, 2)",
        pattern="Two Pointers",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Dutch National Flag. Three pointers: low, mid, high.",
        approach="mid scans array. If 0, swap with low; if 2, swap with high; if 1, advance mid.",
        tags=["array", "two pointers"],
    ),
    Problem(
        name="Squares of a Sorted Array",
        pattern="Two Pointers",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(n)",
        hint="Largest square comes from either end. Fill result from the back.",
        approach="Two pointers at ends. Compare abs values, place larger square at result[end].",
        tags=["array", "two pointers"],
    ),

    # ── Pattern 4: Fast & Slow Pointers ───────────────────────────────────
    Problem(
        name="Middle of the Linked List",
        pattern="Fast & Slow Pointers",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Slow moves 1 step, fast moves 2 steps. When fast reaches end, slow is at middle.",
        approach="Initialize slow=fast=head. While fast and fast.next exist, advance. Return slow.",
        tags=["linked list", "two pointers"],
    ),
    Problem(
        name="Linked List Cycle",
        pattern="Fast & Slow Pointers",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Floyd's algorithm: if slow and fast meet, there's a cycle.",
        approach="Slow moves 1 step, fast moves 2. If they meet, cycle exists.",
        tags=["linked list", "cycle detection"],
    ),
    Problem(
        name="Linked List Cycle II (Find Start)",
        pattern="Fast & Slow Pointers",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="After meeting point, reset one pointer to head. They meet at cycle start.",
        approach="Find meeting point via Floyd. Reset one pointer to head, move both at speed 1.",
        tags=["linked list", "cycle detection"],
    ),
    Problem(
        name="Happy Number",
        pattern="Fast & Slow Pointers",
        difficulty="easy",
        time_complexity="O(log n)",
        space_complexity="O(1)",
        hint="Treat digit-square-sum as a sequence. Cycle means not happy; reaching 1 means happy.",
        approach="Slow computes once, fast computes twice. If fast == 1, return True.",
        tags=["math", "cycle detection"],
    ),
    Problem(
        name="Find the Duplicate Number",
        pattern="Fast & Slow Pointers",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Treat array values as next pointers (like a linked list). Find cycle start.",
        approach="Floyd's cycle detection on nums[i] as next pointer. Cycle start = duplicate.",
        tags=["array", "cycle detection"],
    ),

    # ── Pattern 5: Merge Intervals ─────────────────────────────────────────
    Problem(
        name="Merge Intervals",
        pattern="Merge Intervals",
        difficulty="medium",
        time_complexity="O(n log n)",
        space_complexity="O(n)",
        hint="Sort by start time. Merge if current start <= previous end.",
        approach="Sort. For each interval, if overlaps with last merged, extend end; else append.",
        tags=["array", "sorting", "intervals"],
    ),
    Problem(
        name="Insert Interval",
        pattern="Merge Intervals",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(n)",
        hint="Three phases: add all intervals ending before new one, merge overlapping, add rest.",
        approach="Skip non-overlapping left, merge all overlapping with new interval, append rest.",
        tags=["array", "intervals"],
    ),
    Problem(
        name="Minimum Meeting Rooms",
        pattern="Merge Intervals",
        difficulty="medium",
        time_complexity="O(n log n)",
        space_complexity="O(n)",
        hint="Use a min-heap of end times. If earliest end <= current start, reuse room.",
        approach="Sort by start. Min-heap tracks end times. Pop if end <= start, push new end.",
        tags=["array", "heap", "intervals"],
    ),

    # ── Pattern 6: Cyclic Sort ─────────────────────────────────────────────
    Problem(
        name="Find Missing Number",
        pattern="Cyclic Sort",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Place each number at index = number - 1. Scan for mismatch.",
        approach="Cyclic sort into correct positions. Index where nums[i] != i+1 is missing.",
        tags=["array", "cyclic sort"],
    ),
    Problem(
        name="Find All Missing Numbers",
        pattern="Cyclic Sort",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Same as above but collect all mismatched indices.",
        approach="Cyclic sort. All indices where nums[i] != i+1 are missing numbers.",
        tags=["array", "cyclic sort"],
    ),
    Problem(
        name="Find the Duplicate Number",
        pattern="Cyclic Sort",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="When placing a number, if its correct spot is already occupied by the same number, it's a duplicate.",
        approach="Cyclic sort. When nums[i] == nums[nums[i]-1] (and i != nums[i]-1), duplicate found.",
        tags=["array", "cyclic sort"],
    ),
    Problem(
        name="Find Smallest Missing Positive",
        pattern="Cyclic Sort",
        difficulty="hard",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Ignore numbers <= 0 or > n. Sort the rest. First index with mismatch is the answer.",
        approach="Cyclic sort for 1..n. Scan for first i where nums[i] != i+1; return i+1.",
        tags=["array", "cyclic sort"],
    ),

    # ── Pattern 7: In-place Reversal of LinkedList ─────────────────────────
    Problem(
        name="Reverse a Linked List",
        pattern="In-place Reversal of LinkedList",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Three pointers: prev=None, curr=head, next. Redirect curr.next = prev.",
        approach="Iteratively: save next, point curr.next to prev, advance prev and curr.",
        tags=["linked list", "reversal"],
    ),
    Problem(
        name="Reverse Every K-element Sub-list",
        pattern="In-place Reversal of LinkedList",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Reverse K nodes at a time, connect the tail of each group to head of next.",
        approach="Traverse K nodes, reverse them, record tail. Recurse/iterate for remaining.",
        tags=["linked list", "reversal"],
    ),
    Problem(
        name="Rotate a Linked List",
        pattern="In-place Reversal of LinkedList",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Connect tail to head (make circular). Find new tail at position (n - k % n - 1).",
        approach="Find length + tail. k = k % n. New tail at n-k-1, new head at n-k.",
        tags=["linked list", "reversal"],
    ),
    Problem(
        name="Palindrome Linked List",
        pattern="In-place Reversal of LinkedList",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Find middle, reverse second half, compare with first half.",
        approach="Fast/slow to find mid. Reverse second half. Compare node by node.",
        tags=["linked list", "reversal", "two pointers"],
    ),

    # ── Pattern 8: BFS ─────────────────────────────────────────────────────
    Problem(
        name="Binary Tree Level Order Traversal",
        pattern="Breadth-First Search",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(w)",
        hint="Use a queue. Process all nodes at current level before adding next level.",
        approach="Queue with (node, level). At each dequeue, add children. Group by level.",
        tags=["tree", "bfs"],
    ),
    Problem(
        name="Rotten Oranges",
        pattern="Breadth-First Search",
        difficulty="medium",
        time_complexity="O(m*n)",
        space_complexity="O(m*n)",
        hint="Multi-source BFS starting from all rotten oranges simultaneously.",
        approach="Add all rotten oranges to queue. BFS layer by layer, converting fresh to rotten.",
        tags=["matrix", "bfs", "multi-source"],
    ),
    Problem(
        name="Word Ladder",
        pattern="Breadth-First Search",
        difficulty="hard",
        time_complexity="O(n * L²)",
        space_complexity="O(n)",
        hint="Each transformation is one BFS step. Try changing each character to a-z.",
        approach="BFS from beginWord. For each word, try all single-char changes, add valid dict words.",
        tags=["string", "bfs", "graph"],
    ),
    Problem(
        name="Minimum Depth of Binary Tree",
        pattern="Breadth-First Search",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(w)",
        hint="BFS finds shortest path — stop at first leaf node encountered.",
        approach="Level-order BFS. Return level count when first leaf (no children) is found.",
        tags=["tree", "bfs"],
    ),

    # ── Pattern 9: DFS ─────────────────────────────────────────────────────
    Problem(
        name="Path Sum",
        pattern="Depth-First Search",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(h)",
        hint="Subtract node value from target as you go down. Return True if leaf and target == 0.",
        approach="DFS: at each node reduce target. At leaf, check if target - node.val == 0.",
        tags=["tree", "dfs"],
    ),
    Problem(
        name="All Paths From Source to Target",
        pattern="Depth-First Search",
        difficulty="medium",
        time_complexity="O(2^n * n)",
        space_complexity="O(n)",
        hint="DFS with backtracking. Add current node to path, recurse, then remove (backtrack).",
        approach="DFS from node 0. At each node, recurse to all neighbors. Add to result at target.",
        tags=["graph", "dfs", "backtracking"],
    ),
    Problem(
        name="Is Graph Bipartite?",
        pattern="Depth-First Search",
        difficulty="medium",
        time_complexity="O(V+E)",
        space_complexity="O(V)",
        hint="Try to 2-color the graph. If a neighbor has the same color as current node, not bipartite.",
        approach="DFS with coloring. Assign alternating colors. Return False if conflict found.",
        tags=["graph", "dfs", "coloring"],
    ),
    Problem(
        name="Count Paths for a Sum",
        pattern="Depth-First Search",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(n)",
        hint="Use prefix sums along each root-to-leaf path. Count paths with prefix_sum - target seen before.",
        approach="DFS with running sum dict. At each node, check (current_sum - target) in map.",
        tags=["tree", "dfs", "prefix sum"],
    ),

    # ── Pattern 10: Two Heaps ──────────────────────────────────────────────
    Problem(
        name="Find Median from Data Stream",
        pattern="Two Heaps",
        difficulty="hard",
        time_complexity="O(log n)",
        space_complexity="O(n)",
        hint="Max-heap for lower half, min-heap for upper half. Keep sizes balanced.",
        approach="Push to max_heap, balance by pushing max of max_heap to min_heap. Adjust sizes.",
        tags=["heap", "design", "stream"],
    ),
    Problem(
        name="Sliding Window Median",
        pattern="Two Heaps",
        difficulty="hard",
        time_complexity="O(n log k)",
        space_complexity="O(k)",
        hint="Two heaps + lazy deletion. Remove outgoing element from appropriate heap.",
        approach="Two heaps as above. For each slide, add new, lazy-delete old, rebalance, get median.",
        tags=["heap", "sliding window"],
    ),
    Problem(
        name="Kth Largest Element in Array",
        pattern="Two Heaps",
        difficulty="medium",
        time_complexity="O(n log k)",
        space_complexity="O(k)",
        hint="Maintain a min-heap of size K. The top is always the Kth largest.",
        approach="Push each element. If heap size > k, pop smallest. Final top = Kth largest.",
        tags=["heap", "array"],
    ),

    # ── Pattern 11: Subsets / Backtracking ────────────────────────────────
    Problem(
        name="Subsets",
        pattern="Subsets / Backtracking",
        difficulty="medium",
        time_complexity="O(2^n)",
        space_complexity="O(n)",
        hint="For each element, decide include or not. Build result iteratively or recursively.",
        approach="Start with [[]]. For each num, add num to all existing subsets to create new ones.",
        tags=["array", "backtracking"],
    ),
    Problem(
        name="Combination Sum",
        pattern="Subsets / Backtracking",
        difficulty="medium",
        time_complexity="O(2^n)",
        space_complexity="O(n)",
        hint="DFS with remaining target. Can reuse same element (no index increment).",
        approach="Sort candidates. DFS: include candidate (don't advance i), or skip (advance i).",
        tags=["array", "backtracking"],
    ),
    Problem(
        name="Generate Parentheses",
        pattern="Subsets / Backtracking",
        difficulty="medium",
        time_complexity="O(4^n / √n)",
        space_complexity="O(n)",
        hint="Add '(' if open count < n, add ')' if close count < open count.",
        approach="DFS with open and close counters. Base case: both == n, add to result.",
        tags=["string", "backtracking", "recursion"],
    ),
    Problem(
        name="Permutations",
        pattern="Subsets / Backtracking",
        difficulty="medium",
        time_complexity="O(n!)",
        space_complexity="O(n)",
        hint="Swap current position with all positions from current to end. Backtrack by swapping back.",
        approach="Fix element at each index via swapping. Recurse on remaining. Swap back to restore.",
        tags=["array", "backtracking"],
    ),
    Problem(
        name="Palindrome Partitioning",
        pattern="Subsets / Backtracking",
        difficulty="medium",
        time_complexity="O(n * 2^n)",
        space_complexity="O(n)",
        hint="DFS: try all splits. Only recurse if current substring is a palindrome.",
        approach="DFS with start index. For each end index, if s[start:end] is palindrome, recurse.",
        tags=["string", "backtracking", "dp"],
    ),

    # ── Pattern 12: Modified Binary Search ────────────────────────────────
    Problem(
        name="Search in Rotated Sorted Array",
        pattern="Modified Binary Search",
        difficulty="medium",
        time_complexity="O(log n)",
        space_complexity="O(1)",
        hint="One half is always sorted. Determine which half is sorted, then check if target is in it.",
        approach="Find mid. If left half sorted and target in range, search left; else right.",
        tags=["array", "binary search"],
    ),
    Problem(
        name="Find Minimum in Rotated Sorted Array",
        pattern="Modified Binary Search",
        difficulty="medium",
        time_complexity="O(log n)",
        space_complexity="O(1)",
        hint="The minimum is in the unsorted half. If mid > right, min is in right half.",
        approach="Binary search: if nums[mid] > nums[right], left = mid+1; else right = mid.",
        tags=["array", "binary search"],
    ),
    Problem(
        name="Search Insert Position",
        pattern="Modified Binary Search",
        difficulty="easy",
        time_complexity="O(log n)",
        space_complexity="O(1)",
        hint="Standard binary search. Return left pointer when lo > hi.",
        approach="Binary search. At end, lo = insertion position.",
        tags=["array", "binary search"],
    ),
    Problem(
        name="Bitonic Array Maximum",
        pattern="Modified Binary Search",
        difficulty="easy",
        time_complexity="O(log n)",
        space_complexity="O(1)",
        hint="Binary search: if arr[mid] > arr[mid+1], peak is in left; otherwise in right.",
        approach="If arr[mid] > arr[mid+1], right=mid; else left=mid+1. Return arr[left].",
        tags=["array", "binary search"],
    ),

    # ── Pattern 13: Bitwise XOR ────────────────────────────────────────────
    Problem(
        name="Single Number",
        pattern="Bitwise XOR",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="XOR of same numbers = 0. XOR all elements; pairs cancel out, leaving the unique.",
        approach="result = 0. XOR every element. result holds the single number.",
        tags=["array", "bit manipulation"],
    ),
    Problem(
        name="Missing Number",
        pattern="Bitwise XOR",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="XOR all indices (0..n) with all values. Missing number remains.",
        approach="XOR of 0..n XOR array values. Or use sum formula: n*(n+1)/2 - sum(array).",
        tags=["array", "bit manipulation", "math"],
    ),
    Problem(
        name="Two Single Numbers",
        pattern="Bitwise XOR",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="XOR all to get a^b. Use a set bit to split numbers into two groups, XOR each group.",
        approach="XOR all → x=a^b. Find rightmost set bit. Split array into two groups by that bit.",
        tags=["array", "bit manipulation"],
    ),

    # ── Pattern 14: Top K Elements ─────────────────────────────────────────
    Problem(
        name="Top K Frequent Elements",
        pattern="Top K Elements",
        difficulty="medium",
        time_complexity="O(n log k)",
        space_complexity="O(n)",
        hint="Count frequencies, then use a min-heap of size K to track top K.",
        approach="Counter for frequencies. Min-heap: push (freq, num). Pop if size > k.",
        tags=["array", "heap", "hash map"],
    ),
    Problem(
        name="K Closest Points to Origin",
        pattern="Top K Elements",
        difficulty="medium",
        time_complexity="O(n log k)",
        space_complexity="O(k)",
        hint="Max-heap of size K on distance. Pop if heap exceeds K.",
        approach="Push (-dist, point) to max-heap (negate for Python's min-heap). Maintain size k.",
        tags=["array", "heap", "math"],
    ),
    Problem(
        name="Sliding Window Maximum",
        pattern="Top K Elements",
        difficulty="hard",
        time_complexity="O(n)",
        space_complexity="O(k)",
        hint="Monotonic deque: maintain decreasing order, front is always the maximum.",
        approach="Deque stores indices. Remove out-of-window from front. Remove smaller from back.",
        tags=["array", "deque", "sliding window"],
    ),
    Problem(
        name="Kth Largest Element in a Stream",
        pattern="Top K Elements",
        difficulty="easy",
        time_complexity="O(log k)",
        space_complexity="O(k)",
        hint="Min-heap of size K. The top of heap is always the Kth largest.",
        approach="On add, push to heap. If size > k, pop. Return heap[0].",
        tags=["heap", "design", "stream"],
    ),

    # ── Pattern 15: K-way Merge ────────────────────────────────────────────
    Problem(
        name="Merge K Sorted Lists",
        pattern="K-way Merge",
        difficulty="hard",
        time_complexity="O(n log k)",
        space_complexity="O(k)",
        hint="Min-heap with one element from each list. Always extract smallest and push its next.",
        approach="Push head of each list to min-heap. Pop min, push its next, connect to result.",
        tags=["linked list", "heap", "merge"],
    ),
    Problem(
        name="Find K Pairs with Smallest Sums",
        pattern="K-way Merge",
        difficulty="medium",
        time_complexity="O(k log k)",
        space_complexity="O(k)",
        hint="Start with pairs (nums1[0], nums2[j]). Use heap; when you pop (i,j), push (i+1,j).",
        approach="Heap initialized with (nums1[0]+nums2[j], 0, j) for j in range(min(k,len(nums2))).",
        tags=["array", "heap"],
    ),
    Problem(
        name="Kth Smallest in Sorted Matrix",
        pattern="K-way Merge",
        difficulty="medium",
        time_complexity="O(k log n)",
        space_complexity="O(n)",
        hint="Push first element of each row. Pop min k times.",
        approach="Min-heap with (val, row, col). Pop, push right neighbor. Repeat k times.",
        tags=["matrix", "heap", "binary search"],
    ),

    # ── Pattern 16: Topological Sort ──────────────────────────────────────
    Problem(
        name="Course Schedule",
        pattern="Topological Sort",
        difficulty="medium",
        time_complexity="O(V+E)",
        space_complexity="O(V+E)",
        hint="Build directed graph of prerequisites. Cycle = impossible. Use BFS (Kahn's) or DFS.",
        approach="Build adjacency list + in-degree. BFS: enqueue 0-in-degree nodes. Cycle if not all processed.",
        tags=["graph", "topological sort", "cycle detection"],
    ),
    Problem(
        name="Course Schedule II",
        pattern="Topological Sort",
        difficulty="medium",
        time_complexity="O(V+E)",
        space_complexity="O(V+E)",
        hint="Same as Course Schedule but return the order. Kahn's BFS naturally gives order.",
        approach="Kahn's BFS. Order of dequeue = valid course order. Empty order if cycle.",
        tags=["graph", "topological sort"],
    ),
    Problem(
        name="Alien Dictionary",
        pattern="Topological Sort",
        difficulty="hard",
        time_complexity="O(C)",
        space_complexity="O(1)",
        hint="Compare adjacent words to infer character ordering edges. Then topological sort.",
        approach="Build graph from adjacent word comparisons. Topo sort the character graph.",
        tags=["graph", "topological sort", "string"],
    ),
    Problem(
        name="Minimum Height Trees",
        pattern="Topological Sort",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(n)",
        hint="Iteratively remove leaf nodes (degree 1). The remaining 1-2 nodes are the roots.",
        approach="Repeatedly remove leaves. Add new leaves to queue. Last remaining = answer.",
        tags=["graph", "topological sort", "tree"],
    ),

    # ── Pattern 17: 0/1 Knapsack (DP) ─────────────────────────────────────
    Problem(
        name="0/1 Knapsack Problem",
        pattern="0/1 Knapsack (DP)",
        difficulty="medium",
        time_complexity="O(n*W)",
        space_complexity="O(W)",
        hint="dp[w] = max profit with capacity w. For each item, iterate W down to weight.",
        approach="1D DP array. For each item: for w from W to weight: dp[w] = max(dp[w], dp[w-wt]+val).",
        tags=["dp", "array"],
    ),
    Problem(
        name="Subset Sum",
        pattern="0/1 Knapsack (DP)",
        difficulty="medium",
        time_complexity="O(n*S)",
        space_complexity="O(S)",
        hint="Boolean DP: dp[s] = True if subset with sum s exists.",
        approach="dp[0]=True. For each num, iterate s from target down to num: dp[s] |= dp[s-num].",
        tags=["dp", "array"],
    ),
    Problem(
        name="Equal Subset Sum Partition",
        pattern="0/1 Knapsack (DP)",
        difficulty="medium",
        time_complexity="O(n*S)",
        space_complexity="O(S)",
        hint="If total sum is odd, impossible. Otherwise find subset summing to total/2.",
        approach="Subset Sum problem with target = sum/2.",
        tags=["dp", "array"],
    ),
    Problem(
        name="Target Sum",
        pattern="0/1 Knapsack (DP)",
        difficulty="medium",
        time_complexity="O(n*S)",
        space_complexity="O(S)",
        hint="P - N = target and P + N = sum → P = (sum + target) / 2. Find subsets summing to P.",
        approach="Count subsets summing to (sum+target)/2. If sum+target is odd, return 0.",
        tags=["dp", "array"],
    ),
    Problem(
        name="Coin Change",
        pattern="0/1 Knapsack (DP)",
        difficulty="medium",
        time_complexity="O(n*amount)",
        space_complexity="O(amount)",
        hint="Unbounded knapsack: coins can be reused. dp[amount] = min coins.",
        approach="dp[0]=0, dp[i]=inf. For each coin, for each amount >= coin: dp[a] = min(dp[a], dp[a-c]+1).",
        tags=["dp", "array", "unbounded knapsack"],
    ),

    # ── Pattern 18: Fibonacci Numbers (DP) ────────────────────────────────
    Problem(
        name="Climbing Stairs",
        pattern="Fibonacci Numbers (DP)",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Ways to reach step n = ways to reach n-1 + ways to reach n-2.",
        approach="dp[n] = dp[n-1] + dp[n-2]. Use two rolling variables.",
        tags=["dp", "math"],
    ),
    Problem(
        name="House Robber",
        pattern="Fibonacci Numbers (DP)",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="At each house, choose to rob (skip adjacent) or skip. dp[i] = max(dp[i-1], dp[i-2]+nums[i]).",
        approach="Two rolling variables: prev2, prev1. Update prev2=prev1, prev1=max(prev1, prev2+num).",
        tags=["dp", "array"],
    ),
    Problem(
        name="Jump Game",
        pattern="Fibonacci Numbers (DP)",
        difficulty="medium",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="Track maximum reachable index. If current index > max_reach, return False.",
        approach="max_reach = 0. For each i <= max_reach, update max_reach = max(max_reach, i+nums[i]).",
        tags=["dp", "greedy", "array"],
    ),
    Problem(
        name="N-th Tribonacci Number",
        pattern="Fibonacci Numbers (DP)",
        difficulty="easy",
        time_complexity="O(n)",
        space_complexity="O(1)",
        hint="T(n) = T(n-1) + T(n-2) + T(n-3). Use three rolling variables.",
        approach="Base cases 0,1,1. Roll three variables forward.",
        tags=["dp", "math"],
    ),

    # ── Pattern 19: Palindromic Subsequence (DP) ──────────────────────────
    Problem(
        name="Longest Palindromic Subsequence",
        pattern="Palindromic Subsequence (DP)",
        difficulty="medium",
        time_complexity="O(n²)",
        space_complexity="O(n²)",
        hint="LPS(s) = LCS(s, reverse(s)). Or dp[i][j]: if s[i]==s[j], dp[i][j] = dp[i+1][j-1]+2.",
        approach="Fill 2D dp diagonally. Length-1 substrings have LPS = 1.",
        tags=["dp", "string"],
    ),
    Problem(
        name="Longest Palindromic Substring",
        pattern="Palindromic Subsequence (DP)",
        difficulty="medium",
        time_complexity="O(n²)",
        space_complexity="O(1)",
        hint="Expand around every center (single char and pair). Track max length.",
        approach="For each i, expand around i and (i,i+1). Update start and max_len.",
        tags=["dp", "string", "two pointers"],
    ),
    Problem(
        name="Minimum Insertions to Make String Palindrome",
        pattern="Palindromic Subsequence (DP)",
        difficulty="hard",
        time_complexity="O(n²)",
        space_complexity="O(n²)",
        hint="Answer = n - LPS(s). Characters not in LPS need an inserted mirror character.",
        approach="Find LPS length. Answer = len(s) - LPS.",
        tags=["dp", "string"],
    ),
    Problem(
        name="Count Palindromic Substrings",
        pattern="Palindromic Subsequence (DP)",
        difficulty="medium",
        time_complexity="O(n²)",
        space_complexity="O(1)",
        hint="Expand around each center. Count each valid palindrome found.",
        approach="For each center (odd and even), expand while palindrome. Add to count.",
        tags=["dp", "string", "two pointers"],
    ),

    # ── Pattern 20: Longest Common Substring (DP) ─────────────────────────
    Problem(
        name="Longest Common Subsequence",
        pattern="Longest Common Substring (DP)",
        difficulty="medium",
        time_complexity="O(m*n)",
        space_complexity="O(m*n)",
        hint="If chars match: dp[i][j] = dp[i-1][j-1] + 1. Else: max of skip either char.",
        approach="2D DP. dp[i][j] = dp[i-1][j-1]+1 if match, else max(dp[i-1][j], dp[i][j-1]).",
        tags=["dp", "string"],
    ),
    Problem(
        name="Edit Distance",
        pattern="Longest Common Substring (DP)",
        difficulty="hard",
        time_complexity="O(m*n)",
        space_complexity="O(m*n)",
        hint="dp[i][j] = min operations to convert s1[:i] to s2[:j]. Three choices: insert/delete/replace.",
        approach="If s1[i]==s2[j], dp[i][j]=dp[i-1][j-1]. Else min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])+1.",
        tags=["dp", "string"],
    ),
    Problem(
        name="Shortest Common Supersequence",
        pattern="Longest Common Substring (DP)",
        difficulty="hard",
        time_complexity="O(m*n)",
        space_complexity="O(m*n)",
        hint="SCS length = m + n - LCS length. Build LCS, then merge strings.",
        approach="Find LCS. Merge both strings including LCS chars once, non-LCS chars from both.",
        tags=["dp", "string"],
    ),
    Problem(
        name="Longest Common Subarray",
        pattern="Longest Common Substring (DP)",
        difficulty="medium",
        time_complexity="O(m*n)",
        space_complexity="O(m*n)",
        hint="Contiguous match only. dp[i][j] = dp[i-1][j-1]+1 if match, else 0.",
        approach="2D DP. dp[i][j] = 1+dp[i-1][j-1] if match. Track global max.",
        tags=["dp", "array"],
    ),
]


DIFFICULTY_ORDER = {"easy": 1, "medium": 2, "hard": 3}
DIFFICULTY_EMOJI = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
DIFFICULTY_COLOR = {"easy": "\033[92m", "medium": "\033[93m", "hard": "\033[91m"}
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
BLUE = "\033[94m"


def get_all_patterns() -> list[str]:
    seen = set()
    patterns = []
    for p in PROBLEMS:
        if p.pattern not in seen:
            seen.add(p.pattern)
            patterns.append(p.pattern)
    return patterns


def filter_problems(pattern: Optional[str], difficulty: Optional[str]) -> list[Problem]:
    results = PROBLEMS[:]
    if pattern:
        pattern_lower = pattern.lower()
        results = [p for p in results if pattern_lower in p.pattern.lower()]
    if difficulty:
        results = [p for p in results if p.difficulty == difficulty.lower()]
    return results


def display_problem(problem: Problem, index: int, total: int) -> None:
    diff_emoji = DIFFICULTY_EMOJI[problem.difficulty]
    diff_col = DIFFICULTY_COLOR[problem.difficulty]
    print()
    print(f"{BOLD}{CYAN}{'─'*60}{RESET}")
    print(f"{BOLD}  Problem {index}/{total}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*60}{RESET}")
    print(f"{BOLD}  {problem.name}{RESET}")
    print(f"  Pattern    : {BLUE}{problem.pattern}{RESET}")
    print(f"  Difficulty : {diff_col}{diff_emoji} {problem.difficulty.capitalize()}{RESET}")
    print(f"  Time       : {problem.time_complexity}")
    print(f"  Space      : {problem.space_complexity}")
    print(f"  Tags       : {', '.join(problem.tags)}")
    print()
    print(f"{BOLD}  Hint:{RESET}")
    for line in textwrap.wrap(problem.hint, width=56):
        print(f"    {line}")
    print()
    print(f"{BOLD}  Approach:{RESET}")
    for line in textwrap.wrap(problem.approach, width=56):
        print(f"    {line}")
    print()


def run_interactive_session(problems: list[Problem]) -> None:
    total = len(problems)
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}  DSA Practice Session — {total} question(s){RESET}")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}")
    print("  Press ENTER for next question, 'q' + ENTER to quit.")

    for i, problem in enumerate(problems, 1):
        display_problem(problem, i, total)
        if i < total:
            user_input = input("  [ENTER = next | q = quit] → ").strip().lower()
            if user_input == "q":
                print("\n  Session ended. Keep practicing!\n")
                return

    print(f"\n{BOLD}  Session complete! {total} problem(s) reviewed.{RESET}")
    print("  Next step: implement each solution from scratch.\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Random DSA practice question generator (20 patterns)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python practice_question_generator.py
          python practice_question_generator.py --pattern "Sliding Window"
          python practice_question_generator.py --difficulty easy
          python practice_question_generator.py --count 5
          python practice_question_generator.py --difficulty medium --count 3
          python practice_question_generator.py --list-patterns
        """),
    )
    parser.add_argument("--pattern", "-p", type=str, help="Filter by pattern name (partial match)")
    parser.add_argument(
        "--difficulty", "-d", type=str, choices=["easy", "medium", "hard"], help="Filter by difficulty"
    )
    parser.add_argument("--count", "-c", type=int, default=1, help="Number of questions to generate (default: 1)")
    parser.add_argument("--list-patterns", "-l", action="store_true", help="List all available patterns")
    parser.add_argument("--all", "-a", action="store_true", help="Show all problems (no random selection)")

    args = parser.parse_args()

    if args.list_patterns:
        print(f"\n{BOLD}Available Patterns (20 total):{RESET}\n")
        for i, pattern in enumerate(get_all_patterns(), 1):
            count = sum(1 for p in PROBLEMS if p.pattern == pattern)
            easy = sum(1 for p in PROBLEMS if p.pattern == pattern and p.difficulty == "easy")
            medium = sum(1 for p in PROBLEMS if p.pattern == pattern and p.difficulty == "medium")
            hard = sum(1 for p in PROBLEMS if p.pattern == pattern and p.difficulty == "hard")
            print(f"  {i:2}. {pattern}")
            print(f"      {count} problems — 🟢{easy} easy  🟡{medium} medium  🔴{hard} hard")
        print()
        return

    pool = filter_problems(args.pattern, args.difficulty)

    if not pool:
        print(f"\n  No problems match the given filters. Use --list-patterns to see options.\n")
        return

    if args.all:
        selected = pool
    else:
        count = min(args.count, len(pool))
        selected = random.sample(pool, count)
        selected.sort(key=lambda p: DIFFICULTY_ORDER[p.difficulty])

    run_interactive_session(selected)


if __name__ == "__main__":
    main()
