# Coding Interview Problems

A curated collection of coding problems, patterns, and solutions to help you ace your next technical interview. This repository includes structured problem-solving techniques, pattern-based approaches, and clean Python solutions.

---

## Contents

The repository is organized by **20 proven coding patterns** based on [Data Structure Notes](https://github.com/kumarakshay2456/Data_Structure_Notes) and [Striver's SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/).

---

## 20 Patterns Covered

| # | Pattern | Key Data Structures | Use Case |
|---|---------|-------------------|----------|
| 1 | **Sliding Window** | Array, String, HashTable | Max/Min subarray or substring problems |
| 2 | **Islands / Matrix Traversal** | Matrix, Queue | 2D grid traversal problems |
| 3 | **Two Pointers** | Array, String, LinkedList | Opposite-direction pointer problems |
| 4 | **Fast & Slow Pointers** | Array, LinkedList | Cycle detection, middle element |
| 5 | **Merge Intervals** | Array, Heap | Overlapping interval problems |
| 6 | **Cyclic Sort** | Array | Fixed-range integer array problems |
| 7 | **In-place Reversal of LinkedList** | LinkedList | Reversal without extra memory |
| 8 | **Breadth-First Search (BFS)** | Tree, Graph, Queue | Level-order, shortest path |
| 9 | **Depth-First Search (DFS)** | Tree, Graph, Matrix | Path finding, exhaustive search |
| 10 | **Two Heaps** | Heap, Array | Median, partition into two halves |
| 11 | **Subsets** | Array, Queue, String | Permutations and combinations |
| 12 | **Modified Binary Search** | Array | Search in sorted/rotated arrays |
| 13 | **Bitwise XOR** | Array, Bits | Bit manipulation problems |
| 14 | **Top K Elements** | Array, Heap, Queue | K largest/smallest/frequent |
| 15 | **K-way Merge** | Array, Heap, Queue | Merging sorted arrays/lists |
| 16 | **Topological Sort** | Graph, HashTable, Queue | Dependency ordering |
| 17 | **0/1 Knapsack (DP)** | Array, HashTable | Optimization with constraints |
| 18 | **Fibonacci Numbers (DP)** | Array, HashTable | Sequence-based DP problems |
| 19 | **Palindromic Subsequence (DP)** | Array, String | Palindrome optimization problems |
| 20 | **Longest Common Substring (DP)** | Array, HashTable | String/sequence comparison |

---

## Repository Structure

```
coding-interview-problems/
├── arrays/                          # Array & string problems (40+ files)
│   ├── DP_Problems/                 # Dynamic programming solutions
│   ├── all_types_stock_question/    # Stock buy/sell variants
│   ├── concurrency/                 # Concurrency problems
│   └── *.py                         # Individual problem files
├── link_list/                       # Linked list problems
├── tree/                            # Binary tree & BST problems
├── graph/                           # Graph traversal problems
├── Queue/                           # Queue data structure
├── json/                            # JSON manipulation
├── GO/                              # Go language examples
├── crud_api_implementation_django/  # Django REST API
├── crud_api_implementation_fastapi/ # FastAPI implementation
├── interview_prep/                  # System design notes
│   ├── lld/                         # Low-Level Design (weeks 1-2)
│   └── hld/                         # High-Level Design (weeks 3-4)
├── practice_question_generator.py   # Random practice question generator
├── coding_interview_problems_solutions.md
└── quick_revision.md
```

---

## Pattern Details

### 1. Sliding Window
**When to use:** Finding maximum/minimum subarray or substring satisfying a condition, in O(n).
**Identify by:** Problems with contiguous subarray/substring, given window size K, constraint N <= 10^6.

Sample problems: Maximum Sum Subarray of Size K, Longest Substring Without Repeating Characters, Minimum Window Substring, Find All Anagrams in a String, Fruit Into Baskets.

---

### 2. Islands / Matrix Traversal
**When to use:** Efficiently traversing a 2D matrix/grid.

Sample problems: Number of Islands, Flood Fill, Word Search, Unique Paths, Cycle in a Matrix.

---

### 3. Two Pointers
**When to use:** Iterate through sorted data from two ends simultaneously.

Sample problems: Two Sum II, Container With Most Water, Trapping Rain Water, 3Sum, Sort Colors, Remove Duplicates from Sorted Array.

---

### 4. Fast & Slow Pointers (Hare & Tortoise)
**When to use:** Cycle detection, finding middle of linked list, finding duplicate numbers.

Sample problems: Middle of LinkedList, Happy Number, Linked List Cycle, Linked List Cycle II, Find the Duplicate Number.

---

### 5. Merge Intervals
**When to use:** Dealing with overlapping intervals or merging ranges.

Sample problems: Conflicting Appointments, Minimum Meeting Rooms, Employee Shift Scheduling, Insert Interval.

---

### 6. Cyclic Sort
**When to use:** Array contains numbers in a fixed range (1 to n).

Sample problems: Find Missing Number, Find Duplicate Number, Find All Missing Numbers, Find Smallest Missing Positive, Find Majority Element.

---

### 7. In-place Reversal of LinkedList
**When to use:** Reversing linked list nodes without extra memory.

Sample problems: Reverse a LinkedList, Reverse every K-element Sub-list, Rotate a LinkedList, Palindrome LinkedList, Swap Nodes in Pairs.

---

### 8. Breadth-First Search (BFS)
**When to use:** Level-by-level tree/graph traversal, shortest path in unweighted graph.

Sample problems: Binary Tree Level Order Traversal, Word Ladder, Rotten Oranges, Shortest Path in Grid, Perfect Squares.

---

### 9. Depth-First Search (DFS)
**When to use:** Exhaustive search, path finding, backtracking.

Sample problems: Number of Islands, All Paths From Source to Target, Word Search, Count Paths for a Sum, Is Graph Bipartite.

---

### 10. Two Heaps
**When to use:** Problems requiring smallest element from one part and largest from another (e.g., median).

Sample problems: Find Median of a Number Stream, Sliding Window Median, Find Kth Smallest in Sorted Matrix, Merge K Sorted Lists.

---

### 11. Subsets / Backtracking
**When to use:** Problems asking for permutations, combinations, or subsets of a set.

Sample problems: Subsets, Subsets II, Permutations, Combination Sum, Generate Parentheses, Palindrome Partitioning, Letter Case Permutation.

---

### 12. Modified Binary Search
**When to use:** Search in a sorted, rotated, or partially sorted array.

Sample problems: Search in Rotated Sorted Array, Find Minimum in Rotated Array, Bitonic Array Maximum, Floor/Ceiling of a Number, Search Insert Position.

---

### 13. Bitwise XOR
**When to use:** Problems involving finding a single unique element or missing numbers using bit manipulation.

Sample problems: Single Number, Missing Number, Two Single Numbers, Find All Duplicates, Flipping an Image.

---

### 14. Top K Elements
**When to use:** Finding top/smallest/most frequent K elements without sorting everything.

Sample problems: Top K Frequent Elements, Kth Largest Element, K Closest Points to Origin, Sliding Window Maximum, Kth Largest in a Stream.

---

### 15. K-way Merge
**When to use:** Merging K sorted arrays/lists or finding the Kth smallest across sorted lists.

Sample problems: Merge K Sorted Lists, Kth Smallest in M Sorted Lists, Find K Pairs with Smallest Sums, Find Median from Data Stream.

---

### 16. Topological Sort
**When to use:** Finding linear ordering of elements with dependencies (DAG problems).

Sample problems: Course Schedule, Course Schedule II, Alien Dictionary, Task Scheduling, Minimum Height Trees, Reconstruct Itinerary.

---

### 17. 0/1 Knapsack (Dynamic Programming)
**When to use:** Optimization problems where each element can be picked at most once.

Sample problems: 0/1 Knapsack, Subset Sum, Equal Subset Sum Partition, Target Sum, Minimum Subset Sum Difference, Partition Equal Subset Sum.

---

### 18. Fibonacci Numbers (Dynamic Programming)
**When to use:** Problems following a Fibonacci-like recurrence where answer depends on previous results.

Sample problems: Climbing Stairs, House Robber, N-th Tribonacci Number, Tiling Problem, Staircase, Maximum Product Cutting.

---

### 19. Palindromic Subsequence (Dynamic Programming)
**When to use:** Optimization problems related to palindromic strings/sequences.

Sample problems: Longest Palindromic Subsequence, Longest Palindromic Substring, Minimum Deletion to Make Palindrome, Count Palindromic Subsequences.

---

### 20. Longest Common Substring (Dynamic Programming)
**When to use:** Finding the optimal part of a string/sequence using comparison.

Sample problems: Longest Common Subsequence, Edit Distance, Longest Common Subarray, Shortest Common Supersequence, Longest Palindromic Substring.

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/kumarakshay2456/coding-interview-problems.git
cd coding-interview-problems
```

### Run a Problem File

```bash
python arrays/kadane_algo.py
```

### Generate Random Practice Questions

```bash
python practice_question_generator.py
```

Options:
```bash
python practice_question_generator.py --pattern "Sliding Window"
python practice_question_generator.py --difficulty easy
python practice_question_generator.py --count 5
python practice_question_generator.py --list-patterns
```

---

## Why This Repo?

- Structured by 20 proven interview patterns
- Clean, beginner-friendly Python solutions
- Interview-ready explanations with time/space complexity
- Covers DSA + System Design (HLD + LLD)
- Random practice question generator for daily drill

---

## Interview Prep Notes

The `interview_prep/` folder contains a structured 4-week study plan:

- **Week 1-2 (LLD):** OOP basics, SOLID principles, UML, design patterns (creational, structural, behavioral), Parking Lot, Elevator System, Library System
- **Week 3-4 (HLD):** Networking, Databases, Caching, CAP Theorem, Scalability, Microservices, Message Queues, URL Shortener, Rate Limiter, News Feed

---

## Resources

- [Data Structure Notes (20 Patterns)](https://github.com/kumarakshay2456/Data_Structure_Notes)
- [Striver's SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)

---

## Author

**Akshay Kumar**

[GitHub](https://github.com/kumarakshay2456) • [LinkedIn](https://www.linkedin.com/in/kumarakshay2456)

If you find this repository helpful, give it a star! It motivates me to add more content.
