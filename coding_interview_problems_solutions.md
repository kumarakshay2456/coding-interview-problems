# Coding Interview Problems - Complete Solutions Guide

A comprehensive reference of all solved problems organized by the 20 proven patterns, with time/space complexity analysis.

---

## Table of Contents

1. [Sliding Window](#1-sliding-window)
2. [Islands / Matrix Traversal](#2-islands--matrix-traversal)
3. [Two Pointers](#3-two-pointers)
4. [Fast & Slow Pointers](#4-fast--slow-pointers)
5. [Merge Intervals](#5-merge-intervals)
6. [Cyclic Sort](#6-cyclic-sort)
7. [In-place Reversal of LinkedList](#7-in-place-reversal-of-linkedlist)
8. [Breadth-First Search](#8-breadth-first-search)
9. [Depth-First Search](#9-depth-first-search)
10. [Two Heaps](#10-two-heaps)
11. [Subsets / Backtracking](#11-subsets--backtracking)
12. [Modified Binary Search](#12-modified-binary-search)
13. [Bitwise XOR](#13-bitwise-xor)
14. [Top K Elements](#14-top-k-elements)
15. [K-way Merge](#15-k-way-merge)
16. [Topological Sort](#16-topological-sort)
17. [0/1 Knapsack (DP)](#17-01-knapsack-dp)
18. [Fibonacci Numbers (DP)](#18-fibonacci-numbers-dp)
19. [Palindromic Subsequence (DP)](#19-palindromic-subsequence-dp)
20. [Longest Common Substring (DP)](#20-longest-common-substring-dp)
- [Tree Problems](#tree-problems)
- [Linked List Operations](#linked-list-operations)
- [Graph Algorithms](#graph-algorithms)
- [Mathematical Problems](#mathematical-problems)
- [Stack Problems](#stack-problems)
- [Array Manipulation](#array-manipulation)
- [CRUD API Implementations](#crud-api-implementations)

---

## 1. Sliding Window

**Pattern:** Maintain a window over a sequence and slide it to find optimal subarray/substring.
**Time:** O(n) | **Space:** O(1) to O(k)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Maximum Sum Subarray of Size K | [arrays/maximum_sum_sub_array.py](arrays/maximum_sum_sub_array.py) | O(n) | O(1) | Fixed window |
| Longest Substring Without Repeating Characters | [arrays/longest-substring-without-repeating-characters.py](arrays/longest-substring-without-repeating-characters.py) | O(n) | O(min(m,n)) | Variable window + HashSet |
| Minimum Size Subarray Sum | [arrays/minimum_size_subarray_sum.py](arrays/minimum_size_subarray_sum.py) | O(n) | O(1) | Shrink when condition met |
| Fruit Into Baskets | [arrays/fruit-into-baskets.py](arrays/fruit-into-baskets.py) | O(n) | O(1) | At most 2 distinct |
| Longest Subarray with Ones After Replacement | [arrays/longest_subarray_with_ones_after_replacement.py](arrays/longest_subarray_with_ones_after_replacement.py) | O(n) | O(1) | Count zeros in window |
| Subarray Sum Equals K | [arrays/subarray-sum-equals-k.py](arrays/subarray-sum-equals-k.py) | O(n) | O(n) | Prefix sum |
| Longest Repeating Character Replacement | — | O(n) | O(1) | Max freq in window |
| Subarrays with K Different Integers | — | O(n) | O(k) | Exact K = atMost(K) - atMost(K-1) |
| Minimum Window Substring | — | O(n) | O(k) | Two pointer + freq map |
| Find All Anagrams in a String | — | O(n) | O(k) | Fixed window + freq compare |

---

## 2. Islands / Matrix Traversal

**Pattern:** BFS or DFS on a 2D grid treating cells as graph nodes.
**Time:** O(m*n) | **Space:** O(m*n)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Number of Islands | [graph/count_component.py](graph/count_component.py) | O(m*n) | O(m*n) | DFS flood fill |
| Contiguous Array Equal 0s and 1s | [arrays/contiguous_array_equal_0_and_1.py](arrays/contiguous_array_equal_0_and_1.py) | O(n) | O(n) | Prefix sum trick |
| Flood Fill | — | O(m*n) | O(m*n) | BFS/DFS |
| Unique Paths | — | O(m*n) | O(m*n) | DP grid |
| Word Search | — | O(m*n*4^L) | O(L) | DFS + backtrack |

---

## 3. Two Pointers

**Pattern:** Two indices moving toward each other or in same direction to reduce O(n²) to O(n).
**Time:** O(n) | **Space:** O(1)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Container With Most Water | [arrays/container_with_most_water.py](arrays/container_with_most_water.py) | O(n) | O(1) | Shrink smaller height side |
| Trapping Rain Water | [arrays/trapping_rain_water.py](arrays/trapping_rain_water.py) | O(n) | O(1) | Track left/right max |
| Sort Colors (0, 1, 2) | [arrays/sort_0_1_2.py](arrays/sort_0_1_2.py) | O(n) | O(1) | Dutch National Flag |
| Squares of a Sorted Array | [arrays/squares_of_a_sorted_array.py](arrays/squares_of_a_sorted_array.py) | O(n) | O(n) | Fill from end |
| Two Sum (unsorted) | [arrays/two_sum_without_sorting.py](arrays/two_sum_without_sorting.py) | O(n) | O(n) | Hash map |
| Two Sum II and III (sorted) | [arrays/two_sum_ii_and_iii_input_array_is_sorted.py](arrays/two_sum_ii_and_iii_input_array_is_sorted.py) | O(n) | O(1) | Sorted array |
| Shortest Unsorted Continuous Subarray | [arrays/shortest_unsorted_continuous_subarray.py](arrays/shortest_unsorted_continuous_subarray.py) | O(n) | O(1) | Find boundary violation |
| 3Sum | — | O(n²) | O(1) | Sort + two pointers |
| Remove Duplicates from Sorted Array | — | O(n) | O(1) | Slow/fast pointer |

---

## 4. Fast & Slow Pointers

**Pattern:** Hare & Tortoise — two pointers at different speeds to detect cycles or midpoints.
**Time:** O(n) | **Space:** O(1)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Middle of Linked List | [link_list/find_middle_element.py](link_list/find_middle_element.py) | O(n) | O(1) | Fast moves 2x |
| Linked List Cycle | [link_list/link_list_cycle.py](link_list/link_list_cycle.py) | O(n) | O(1) | Floyd's algorithm |
| Linked List Cycle II (start) | [link_list/link_list_cycle_2.py](link_list/link_list_cycle_2.py) | O(n) | O(1) | Reset one pointer to head |
| Happy Number | [arrays/find_happy_number.py](arrays/find_happy_number.py) | O(log n) | O(1) | Detect cycle in seq |
| Find the Duplicate Number | — | O(n) | O(1) | Treat as linked list |

---

## 5. Merge Intervals

**Pattern:** Sort intervals by start time, then merge or check overlaps.
**Time:** O(n log n) | **Space:** O(n)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Conflicting Appointments | [arrays/metting_overlap_prob.py](arrays/metting_overlap_prob.py) | O(n log n) | O(1) | Check adjacent |
| Job Scheduling | [arrays/job_scheduling.py](arrays/job_scheduling.py) | O(n log n) | O(n) | Greedy + sort |
| Merge Intervals | — | O(n log n) | O(n) | Sort + merge |
| Insert Interval | — | O(n) | O(n) | Merge with new interval |
| Minimum Meeting Rooms | — | O(n log n) | O(n) | Min heap of end times |

---

## 6. Cyclic Sort

**Pattern:** Place each number at its correct index (number i goes to index i-1).
**Time:** O(n) | **Space:** O(1)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Sort Array 0s 1s 2s | [arrays/sort_0_1_2.py](arrays/sort_0_1_2.py) | O(n) | O(1) | Dutch National Flag |
| Majority Element | [arrays/majority_element.py](arrays/majority_element.py) | O(n) | O(1) | Boyer-Moore voting |
| Find Missing Number | — | O(n) | O(1) | After cyclic sort, scan |
| Find Duplicate Number | — | O(n) | O(1) | Misplaced = duplicate |
| Find All Missing Numbers | — | O(n) | O(1) | Collect all misplaced |
| Find Smallest Missing Positive | — | O(n) | O(1) | Cyclic sort 1..n |

---

## 7. In-place Reversal of LinkedList

**Pattern:** Reverse pointers between nodes without using extra memory.
**Time:** O(n) | **Space:** O(1)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Reverse a LinkedList | [link_list/reverse_ll.py](link_list/reverse_ll.py) | O(n) | O(1) | Three pointer technique |
| Reverse Every K-element Sub-list | [link_list/reverse_in_group.py](link_list/reverse_in_group.py) | O(n) | O(1) | Group-wise reversal |
| Reverse Between Two Pointers | [link_list/reverse_ll_between_two_pointer.py](link_list/reverse_ll_between_two_pointer.py) | O(n) | O(1) | Partial reversal |
| Reverse with Specific Index | [link_list/reverse_link_list_with_specific_index.py](link_list/reverse_link_list_with_specific_index.py) | O(n) | O(1) | Indexed reversal |
| Palindrome LinkedList | — | O(n) | O(1) | Reverse second half |

---

## 8. Breadth-First Search

**Pattern:** Explore all neighbors at current depth before going deeper. Uses a queue.
**Time:** O(V+E) | **Space:** O(V)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| BFS Traversal | [graph/bfs_and_dfs.py](graph/bfs_and_dfs.py) | O(V+E) | O(V) | Queue-based |
| Level Order Traversal | [tree/level_order_traversal.py](tree/level_order_traversal.py) | O(n) | O(w) | w = max width |
| Shortest Path (unweighted) | [graph/shortest_path.py](graph/shortest_path.py) | O(V+E) | O(V) | BFS guarantees shortest |
| Shortest Path v2 | [graph/shortest_path_v2.py](graph/shortest_path_v2.py) | O(V+E) | O(V) | Enhanced BFS |
| Rotten Oranges | — | O(m*n) | O(m*n) | Multi-source BFS |
| Word Ladder | — | O(n*L²) | O(n) | Character-by-character BFS |
| Minimum Depth of Binary Tree | — | O(n) | O(w) | Stop at first leaf |

---

## 9. Depth-First Search

**Pattern:** Explore as far as possible before backtracking. Uses recursion or explicit stack.
**Time:** O(V+E) | **Space:** O(V)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| DFS Traversal | [graph/bfs_and_dfs.py](graph/bfs_and_dfs.py) | O(V+E) | O(V) | Stack/recursion |
| Count Components | [graph/count_component.py](graph/count_component.py) | O(V+E) | O(V) | DFS per unvisited node |
| Basic Graph Ops | [graph/basic_repratition.py](graph/basic_repratition.py) | O(V+E) | O(V) | Adjacency list DFS |
| Tree Traversals (In/Pre/Post) | [tree/traversals.py](tree/traversals.py) | O(n) | O(h) | Recursive DFS |
| Tree Are Identical | [tree/tree_are_identical.py](tree/tree_are_identical.py) | O(min(n1,n2)) | O(min(h1,h2)) | Recursive DFS compare |
| Number of Islands | — | O(m*n) | O(m*n) | Flood fill DFS |
| All Paths From Source to Target | — | O(2^n * n) | O(n) | DFS + backtracking |
| Is Graph Bipartite? | — | O(V+E) | O(V) | DFS 2-coloring |

---

## 10. Two Heaps

**Pattern:** Maintain a max-heap for lower half and min-heap for upper half of data.
**Time:** O(log n) per insert | **Space:** O(n)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Kth Largest Element | — | O(n log k) | O(k) | Min-heap of size k |
| Find Median from Data Stream | — | O(log n) | O(n) | Balance two heaps |
| Sliding Window Median | — | O(n log k) | O(k) | Two heaps + lazy delete |

---

## 11. Subsets / Backtracking

**Pattern:** Build solution incrementally, backtrack when path is invalid or complete.
**Time:** O(2^n) for subsets, O(n!) for permutations | **Space:** O(n)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Generate Subsets | — | O(2^n) | O(n) | Include/exclude each elem |
| Combination Sum | — | O(2^n) | O(n) | Allow repeats |
| Generate Parentheses | — | O(4^n/√n) | O(n) | Catalan number |
| Permutations | — | O(n!) | O(n) | Swap + backtrack |
| Palindrome Partitioning | — | O(n*2^n) | O(n) | DFS + palindrome check |

---

## 12. Modified Binary Search

**Pattern:** Adapt binary search for rotated arrays, infinite arrays, or finding boundaries.
**Time:** O(log n) | **Space:** O(1)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Two Sum II (sorted) | [arrays/two_sum_ii_and_iii_input_array_is_sorted.py](arrays/two_sum_ii_and_iii_input_array_is_sorted.py) | O(n) | O(1) | Two pointer variant |
| Search in Rotated Array | — | O(log n) | O(1) | Identify sorted half |
| Find Min in Rotated Array | — | O(log n) | O(1) | Track minimum |
| Peak Index in Mountain Array | — | O(log n) | O(1) | Binary search on slope |
| Search Insert Position | — | O(log n) | O(1) | Lower bound |

---

## 13. Bitwise XOR

**Pattern:** XOR same values cancel out (a^a=0, a^0=a). Use to find unique/missing elements.
**Time:** O(n) | **Space:** O(1)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Single Number | — | O(n) | O(1) | XOR all elements |
| Missing Number | — | O(n) | O(1) | XOR with 1..n |
| Find All Duplicates | — | O(n) | O(1) | Sign-flip technique |
| Flipping an Image | — | O(n) | O(1) | Flip + XOR |
| Two Single Numbers | — | O(n) | O(1) | Split by differing bit |

---

## 14. Top K Elements

**Pattern:** Use a heap of size K to maintain the K best elements without full sorting.
**Time:** O(n log k) | **Space:** O(k)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Top K Frequent Elements | — | O(n log k) | O(n) | Min-heap + freq map |
| Kth Largest Element | — | O(n log k) | O(k) | Min-heap of size k |
| K Closest Points to Origin | — | O(n log k) | O(k) | Max-heap by distance |
| Sliding Window Maximum | — | O(n) | O(k) | Monotonic deque |
| Kth Largest in a Stream | — | O(log k) | O(k) | Min-heap, maintain size k |

---

## 15. K-way Merge

**Pattern:** Merge K sorted lists/arrays using a min-heap to always extract the smallest.
**Time:** O(n log k) | **Space:** O(k)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Merge Two Sorted Arrays | [arrays/merge_two_sorted_array.py](arrays/merge_two_sorted_array.py) | O(n+m) | O(1) | In-place merge |
| Merge Arrays | [arrays/merge_array.py](arrays/merge_array.py) | O(n+m) | O(n+m) | New array merge |
| Merge K Sorted Lists | — | O(n log k) | O(k) | Min-heap with list pointer |
| Find K Pairs with Smallest Sums | — | O(k log k) | O(k) | Min-heap with pairs |
| Find Median from Data Stream | — | O(log n) | O(n) | Two heaps approach |

---

## 16. Topological Sort

**Pattern:** BFS with in-degree tracking (Kahn's) or DFS post-order on a DAG.
**Time:** O(V+E) | **Space:** O(V)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Task Scheduling | [arrays/job_scheduling.py](arrays/job_scheduling.py) | O(n log n) | O(n) | Greedy + sort |
| Course Schedule | — | O(V+E) | O(V) | Cycle detection |
| Course Schedule II | — | O(V+E) | O(V) | Return order |
| Alien Dictionary | — | O(V+E) | O(V) | Build graph from order |
| Minimum Height Trees | — | O(V) | O(V) | Prune leaves iteratively |

---

## 17. 0/1 Knapsack (DP)

**Pattern:** dp[i][w] = max value using first i items with weight capacity w.
**Time:** O(n*W) | **Space:** O(W) with optimization

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Climbing Stairs | [arrays/DP_Problems/climbing-stairs.py](arrays/DP_Problems/climbing-stairs.py) | O(n) | O(1) | Fibonacci DP |
| Coin Change | [arrays/DP_Problems/coin_change.py](arrays/DP_Problems/coin_change.py) | O(n*amount) | O(amount) | Unbounded knapsack |
| Coin Change II | [arrays/DP_Problems/coin_change_2.py](arrays/DP_Problems/coin_change_2.py) | O(n*amount) | O(amount) | Count combinations |
| House Robber | [arrays/DP_Problems/house-robber.py](arrays/DP_Problems/house-robber.py) | O(n) | O(1) | State machine DP |
| Jump Game I | [arrays/DP_Problems/jum_game_1.py](arrays/DP_Problems/jum_game_1.py) | O(n) | O(1) | Greedy with DP |
| Target Sum | [arrays/DP_Problems/target_sum_2.py](arrays/DP_Problems/target_sum_2.py) | O(n*sum) | O(sum) | Subset with target |
| Maximum Sum Subarray | [arrays/maximum_sum_sub_array.py](arrays/maximum_sum_sub_array.py) | O(n) | O(1) | Kadane's |
| Equal Subset Sum Partition | — | O(n*sum) | O(sum) | Boolean knapsack |
| Minimum Subset Sum Difference | — | O(n*sum) | O(sum) | Two closest subsets |

---

## 18. Fibonacci Numbers (DP)

**Pattern:** Each result depends on a fixed number of previous results. Build bottom-up.
**Time:** O(n) | **Space:** O(1) with rolling variables

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Climbing Stairs | [arrays/DP_Problems/climbing-stairs.py](arrays/DP_Problems/climbing-stairs.py) | O(n) | O(1) | dp[n] = dp[n-1] + dp[n-2] |
| House Robber | [arrays/DP_Problems/house-robber.py](arrays/DP_Problems/house-robber.py) | O(n) | O(1) | dp[i] = max(dp[i-1], dp[i-2]+nums[i]) |
| Maximum Subarray (Kadane's) | [arrays/kadane_algo.py](arrays/kadane_algo.py) | O(n) | O(1) | Rolling max sum |
| Jump Game | [arrays/DP_Problems/jum_game_1.py](arrays/DP_Problems/jum_game_1.py) | O(n) | O(1) | Rolling max reach |
| Pascal's Triangle | [arrays/pascals_triangle.py](arrays/pascals_triangle.py) | O(n²) | O(n²) | Each row from previous |

---

## 19. Palindromic Subsequence (DP)

**Pattern:** dp[i][j] = result for substring s[i..j]. Fill diagonally.
**Time:** O(n²) | **Space:** O(n²)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Longest Palindrome (Substring) | [arrays/longest_palindrome.py](arrays/longest_palindrome.py) | O(n²) | O(1) | Expand around center |
| Longest Palindromic Subsequence | — | O(n²) | O(n²) | LCS with reversed string |
| Minimum Deletion for Palindrome | — | O(n²) | O(n²) | n - LPS length |
| Count Palindromic Substrings | — | O(n²) | O(1) | Expand around center |
| Palindrome Partitioning | — | O(n²) | O(n²) | Min cuts + is_palindrome |

---

## 20. Longest Common Substring (DP)

**Pattern:** dp[i][j] = result for first i chars of s1 and first j chars of s2.
**Time:** O(m*n) | **Space:** O(m*n)

| Problem | File | Time | Space | Notes |
|---------|------|------|-------|-------|
| Longest Common Subsequence | — | O(m*n) | O(m*n) | Classic LCS |
| Edit Distance | — | O(m*n) | O(m*n) | Insert/delete/replace |
| Longest Common Subarray | — | O(m*n) | O(m*n) | Contiguous match |
| Shortest Common Supersequence | — | O(m*n) | O(m*n) | LCS + combine |

---

## Tree Problems

| Problem | File | Time | Space | Pattern |
|---------|------|------|-------|---------|
| BST Insert/Search/Min/Max | [tree/bst.py](tree/bst.py) | O(h) | O(h) | BST property |
| Inorder/Preorder/Postorder | [tree/traversals.py](tree/traversals.py) | O(n) | O(h) | DFS |
| Level Order Traversal | [tree/level_order_traversal.py](tree/level_order_traversal.py) | O(n) | O(w) | BFS |
| Tree Are Identical | [tree/tree_are_identical.py](tree/tree_are_identical.py) | O(min(n1,n2)) | O(min(h1,h2)) | Recursive DFS |
| Balance Tree Check | [arrays/tree/balance_tree.py](arrays/tree/balance_tree.py) | O(n) | O(h) | Height check |

---

## Linked List Operations

| Problem | File | Time | Space | Pattern |
|---------|------|------|-------|---------|
| Add New Element | [link_list/add_new_element.py](link_list/add_new_element.py) | O(n) | O(1) | Traversal |
| Print Elements | [link_list/print_element.py](link_list/print_element.py) | O(n) | O(1) | Traversal |
| Reverse Linked List | [link_list/reverse_ll.py](link_list/reverse_ll.py) | O(n) | O(1) | Three Pointers |
| Reverse in Group | [link_list/reverse_in_group.py](link_list/reverse_in_group.py) | O(n) | O(1) | K-group reversal |
| Reverse Between Pointers | [link_list/reverse_ll_between_two_pointer.py](link_list/reverse_ll_between_two_pointer.py) | O(n) | O(1) | Partial reversal |
| Reverse with Specific Index | [link_list/reverse_link_list_with_specific_index.py](link_list/reverse_link_list_with_specific_index.py) | O(n) | O(1) | Indexed reversal |
| Find Middle | [link_list/find_middle_element.py](link_list/find_middle_element.py) | O(n) | O(1) | Fast/Slow pointers |
| Cycle Detection | [link_list/link_list_cycle.py](link_list/link_list_cycle.py) | O(n) | O(1) | Floyd's algorithm |
| Cycle Start Detection | [link_list/link_list_cycle_2.py](link_list/link_list_cycle_2.py) | O(n) | O(1) | Reset + re-meet |

---

## Graph Algorithms

| Problem | File | Time | Space | Pattern |
|---------|------|------|-------|---------|
| BFS and DFS | [graph/bfs_and_dfs.py](graph/bfs_and_dfs.py) | O(V+E) | O(V) | Graph traversal |
| Shortest Path | [graph/shortest_path.py](graph/shortest_path.py) | O(V+E) | O(V) | BFS |
| Shortest Path v2 | [graph/shortest_path_v2.py](graph/shortest_path_v2.py) | O(V+E) | O(V) | Enhanced BFS |
| Count Components | [graph/count_component.py](graph/count_component.py) | O(V+E) | O(V) | DFS |
| Basic Graph Ops | [graph/basic_repratition.py](graph/basic_repratition.py) | O(V+E) | O(V) | Adjacency list |

---

## Mathematical Problems

| Problem | File | Time | Space | Pattern |
|---------|------|------|-------|---------|
| Factorial | [arrays/factorial_program.py](arrays/factorial_program.py) | O(n) | O(1) iterative | Math |
| Happy Number | [arrays/find_happy_number.py](arrays/find_happy_number.py) | O(log n) | O(1) | Fast/Slow pointers |
| Pascal's Triangle | [arrays/pascals_triangle.py](arrays/pascals_triangle.py) | O(n²) | O(n²) | DP |
| Majority Element | [arrays/majority_element.py](arrays/majority_element.py) | O(n) | O(1) | Boyer-Moore voting |
| Next Permutation | [arrays/next_permutation.py](arrays/next_permutation.py) | O(n) | O(1) | Lexicographic order |
| Max Profit (stocks) | [arrays/max_profit.py](arrays/max_profit.py) | O(n) | O(1) | Greedy |
| Max Profit (all types) | [arrays/all_types_stock_question/max_profit.py](arrays/all_types_stock_question/max_profit.py) | O(n) | O(1) | Multiple strategies |
| Set Matrix Zero | [arrays/set_matrix_zero.py](arrays/set_matrix_zero.py) | O(m*n) | O(1) | In-place marking |
| Rotate Matrix | [arrays/rotate_matrix.py](arrays/rotate_matrix.py) | O(n²) | O(1) | Transpose + reverse |
| Convert Dict Keys to camelCase | [arrays/convert_dict_key_in_camel_case.py](arrays/convert_dict_key_in_camel_case.py) | O(n) | O(n) | String manipulation |

---

## Stack Problems

| Problem | File | Time | Space | Pattern |
|---------|------|------|-------|---------|
| Stack-based Questions | [arrays/stack_based_question.py](arrays/stack_based_question.py) | Varies | O(n) | Stack |

---

## Array Manipulation

| Problem | File | Time | Space | Pattern |
|---------|------|------|-------|---------|
| Kadane's Algorithm | [arrays/kadane_algo.py](arrays/kadane_algo.py) | O(n) | O(1) | Max subarray sum |
| Maximum Sum Subarray | [arrays/maximum_sum_sub_array.py](arrays/maximum_sum_sub_array.py) | O(n) | O(1) | Kadane's with indices |
| Merge Arrays | [arrays/merge_array.py](arrays/merge_array.py) | O(n+m) | O(n+m) | Two sorted arrays |
| Merge Two Sorted Arrays | [arrays/merge_two_sorted_array.py](arrays/merge_two_sorted_array.py) | O(n+m) | O(1) | In-place |
| Contiguous Subarray Sum K | [arrays/contiguous_sub_array_with_sum_k.py](arrays/contiguous_sub_array_with_sum_k.py) | O(n) | O(n) | Prefix sum |
| Contiguous Array (0s and 1s) | [arrays/contiguous_array_equal_0_and_1.py](arrays/contiguous_array_equal_0_and_1.py) | O(n) | O(n) | Prefix sum |
| Subarray Sum Equals K | [arrays/subarray-sum-equals-k.py](arrays/subarray-sum-equals-k.py) | O(n) | O(n) | Prefix sum |
| Shortest Unsorted Subarray | [arrays/shortest_unsorted_continuous_subarray.py](arrays/shortest_unsorted_continuous_subarray.py) | O(n) | O(1) | Two pointer |
| Concurrency Problems | [arrays/concurrency/concurrency.py](arrays/concurrency/concurrency.py) | Varies | Varies | Thread safety |

---

## CRUD API Implementations

| Implementation | Directory | Framework | Pattern |
|----------------|-----------|-----------|---------|
| Django REST API | [crud_api_implementation_django/ticketing/](crud_api_implementation_django/ticketing/) | Django + DRF | MVS (Model-View-Serializer) |
| FastAPI | [crud_api_implementation_fastapi/events.py](crud_api_implementation_fastapi/events.py) | FastAPI + Pydantic | Async REST API |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Total Problems Tracked | 80+ |
| Patterns Covered | 20 |
| Data Structures | Arrays, Trees, Graphs, LinkedLists, Stacks, Queues, Heaps |
| Algorithm Types | DP, Greedy, Two Pointers, Sliding Window, BFS/DFS, Backtracking, Binary Search |
| Languages | Python, Go |
| Frameworks | Django, FastAPI |

---

## How to Use This Guide

1. **Identify the pattern** from the problem description
2. **Click the file link** to open the solution directly
3. **Study the time/space complexity** before coding
4. **Practice variations** using the random generator: `python practice_question_generator.py`

---

## Additional Resources

- [Data Structure Notes (20 Patterns)](https://github.com/kumarakshay2456/Data_Structure_Notes)
- [Striver's SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)
