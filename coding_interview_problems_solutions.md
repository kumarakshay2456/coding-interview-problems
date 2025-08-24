# 🧠 Coding Interview Problems - Complete Solutions Guide

A comprehensive collection of all solved problems organized by pattern with solutions, time complexity, and space complexity analysis.

---

## 📋 Table of Contents

- [Sliding Window](#sliding-window)
- [Two Pointers](#two-pointers)
- [Dynamic Programming](#dynamic-programming)
- [Tree Traversals](#tree-traversals)
- [Linked List Operations](#linked-list-operations)
- [Graph Algorithms](#graph-algorithms)
- [Array Manipulation](#array-manipulation)
- [String Problems](#string-problems)
- [Stack & Queue](#stack--queue)
- [Binary Search](#binary-search)
- [Greedy Algorithms](#greedy-algorithms)
- [Go Programming](#go-programming)
- [CRUD API Implementations](#crud-api-implementations)
- [Queue Data Structure](#queue-data-structure)
- [JSON Operations](#json-operations)

---

## 🔄 Sliding Window

### 1. Longest Substring Without Repeating Characters
**File**: <a href="arrays/longest-substring-without-repeating-characters.py" target="_blank">arrays/longest-substring-without-repeating-characters.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(min(m, n)) where m is charset size
- **Pattern**: Sliding Window with Hash Set

### 2. Longest Subarray with Ones After Replacement
**File**: <a href="arrays/longest_subarray_with_ones_after_replacement.py" target="_blank">arrays/longest_subarray_with_ones_after_replacement.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Sliding Window with Count

### 3. Minimum Size Subarray Sum
**File**: <a href="arrays/minimum_size_subarray_sum.py" target="_blank">arrays/minimum_size_subarray_sum.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Sliding Window with Sum Tracking

### 4. Fruit Into Baskets
**File**: <a href="arrays/fruit-into-baskets.py" target="_blank">arrays/fruit-into-baskets.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Sliding Window with Two Types

---

## 👆 Two Pointers

### 1. Container With Most Water
**File**: <a href="arrays/container_with_most_water.py" target="_blank">arrays/container_with_most_water.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Two Pointers from Ends

### 2. Trapping Rain Water
**File**: <a href="arrays/trapping_rain_water.py" target="_blank">arrays/trapping_rain_water.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Two Pointers with Height Tracking

### 3. Sort Colors (0, 1, 2)
**File**: <a href="arrays/sort_0_1_2.py" target="_blank">arrays/sort_0_1_2.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Three Pointers (Dutch National Flag)

### 4. Squares of a Sorted Array
**File**: <a href="arrays/squares_of_a_sorted_array.py" target="_blank">arrays/squares_of_a_sorted_array.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(n)
- **Pattern**: Two Pointers from Ends

---

## 🎯 Dynamic Programming

### 1. Climbing Stairs
**File**: <a href="arrays/DP_Problems/climbing-stairs.py" target="_blank">arrays/DP_Problems/climbing-stairs.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Fibonacci Sequence DP

### 2. Coin Change
**File**: <a href="arrays/DP_Problems/coin_change.py" target="_blank">arrays/DP_Problems/coin_change.py</a>
- **Time Complexity**: O(amount * len(coins))
- **Space Complexity**: O(amount)
- **Pattern**: Unbounded Knapsack

### 3. Coin Change II (Combinations)
**File**: <a href="arrays/DP_Problems/coin_change_2.py" target="_blank">arrays/DP_Problems/coin_change_2.py</a>
- **Time Complexity**: O(amount * len(coins))
- **Space Complexity**: O(amount)
- **Pattern**: Unbounded Knapsack Combinations

### 4. House Robber
**File**: <a href="arrays/DP_Problems/house-robber.py" target="_blank">arrays/DP_Problems/house-robber.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: State Machine DP

### 5. Jump Game I
**File**: <a href="arrays/DP_Problems/jum_game_1.py" target="_blank">arrays/DP_Problems/jum_game_1.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Greedy with DP

### 6. Target Sum
**File**: <a href="arrays/DP_Problems/target_sum_2.py" target="_blank">arrays/DP_Problems/target_sum_2.py</a>
- **Time Complexity**: O(n * sum)
- **Space Complexity**: O(n * sum)
- **Pattern**: Subset Sum with Target

---

## 🌳 Tree Traversals

### 1. Binary Search Tree Operations
**File**: <a href="tree/bst.py" target="_blank">tree/bst.py</a>
- **Insert**: O(h) time, O(h) space (recursive)
- **Search**: O(h) time, O(h) space (recursive)
- **Min/Max**: O(h) time, O(1) space
- **Pattern**: BST Property Maintenance

### 2. Tree Traversals
**File**: <a href="tree/traversals.py" target="_blank">tree/traversals.py</a>
- **Inorder**: O(n) time, O(h) space
- **Preorder**: O(n) time, O(h) space
- **Postorder**: O(n) time, O(h) space
- **Level Order**: O(n) time, O(w) space
- **Pattern**: Recursive and Iterative Approaches

### 3. Level Order Traversal
**File**: <a href="tree/level_order_traversal.py" target="_blank">tree/level_order_traversal.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(w) where w is max width
- **Pattern**: BFS with Level Tracking

### 4. Tree Properties
**File**: <a href="tree/tree_are_identical.py" target="_blank">tree/tree_are_identical.py</a>
- **Time Complexity**: O(min(n1, n2))
- **Space Complexity**: O(min(h1, h2))
- **Pattern**: Recursive Comparison

### 5. Balance Tree Check
**File**: <a href="tree/balance_tree.py" target="_blank">tree/balance_tree.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(h)
- **Pattern**: Height Balance Check

---

## 🔗 Linked List Operations

### 1. Basic Operations
**File**: <a href="link_list/add_new_element.py" target="_blank">link_list/add_new_element.py</a>
- **Add**: O(n) time, O(1) space
- **Print**: O(n) time, O(1) space
- **Pattern**: Traversal and Modification

### 2. Reverse Operations
**File**: <a href="link_list/reverse_ll.py" target="_blank">link_list/reverse_ll.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Three Pointer Technique

**File**: <a href="link_list/reverse_in_group.py" target="_blank">link_list/reverse_in_group.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Group-wise Reversal

**File**: <a href="link_list/reverse_ll_between_two_pointer.py" target="_blank">link_list/reverse_ll_between_two_pointer.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Partial List Reversal

### 3. Cycle Detection
**File**: <a href="link_list/link_list_cycle.py" target="_blank">link_list/link_list_cycle.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Floyd's Cycle Finding

**File**: <a href="link_list/link_list_cycle_2.py" target="_blank">link_list/link_list_cycle_2.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Cycle Start Detection

### 4. Middle Element
**File**: <a href="link_list/find_middle_element.py" target="_blank">link_list/find_middle_element.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Fast and Slow Pointers

---

## 🕸️ Graph Algorithms

### 1. BFS and DFS
**File**: <a href="graph/bfs_and_dfs.py" target="_blank">graph/bfs_and_dfs.py</a>
- **BFS**: O(V + E) time, O(V) space
- **DFS**: O(V + E) time, O(V) space
- **Pattern**: Graph Traversal Algorithms

### 2. Shortest Path
**File**: <a href="graph/shortest_path.py" target="_blank">graph/shortest_path.py</a>
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Pattern**: BFS for Unweighted Graphs

**File**: <a href="graph/shortest_path_v2.py" target="_blank">graph/shortest_path_v2.py</a>
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Pattern**: Enhanced BFS Implementation

### 3. Connected Components
**File**: <a href="graph/count_component.py" target="_blank">graph/count_component.py</a>
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Pattern**: DFS Component Counting

---

## 📊 Array Manipulation

### 1. Kadane's Algorithm
**File**: <a href="arrays/kadane_algo.py" target="_blank">arrays/kadane_algo.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Maximum Subarray Sum

### 2. Maximum Sum Subarray
**File**: <a href="arrays/maximum_sum_sub_array.py" target="_blank">arrays/maximum_sum_sub_array.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Kadane's with Indices

### 3. Merge Operations
**File**: <a href="arrays/merge_array.py" target="_blank">arrays/merge_array.py</a>
- **Time Complexity**: O(n + m)
- **Space Complexity**: O(n + m)
- **Pattern**: Two Sorted Arrays Merge

**File**: <a href="arrays/merge_two_sorted_array.py" target="_blank">arrays/merge_two_sorted_array.py</a>
- **Time Complexity**: O(n + m)
- **Space Complexity**: O(1)
- **Pattern**: In-place Merge

### 4. Matrix Operations
**File**: <a href="arrays/rotate_matrix.py" target="_blank">arrays/rotate_matrix.py</a>
- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Pattern**: Layer-wise Rotation

**File**: <a href="arrays/set_matrix_zero.py" target="_blank">arrays/set_matrix_zero.py</a>
- **Time Complexity**: O(m * n)
- **Space Complexity**: O(1)
- **Pattern**: In-place Matrix Modification

### 5. Subarray Problems
**File**: <a href="arrays/contiguous_sub_array_with_sum_k.py" target="_blank">arrays/contiguous_sub_array_with_sum_k.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(n)
- **Pattern**: Prefix Sum with Hash Map

**File**: <a href="arrays/contiguous_array_equal_0_and_1.py" target="_blank">arrays/contiguous_array_equal_0_and_1.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(n)
- **Pattern**: Prefix Sum for Binary Arrays

---

## 🔤 String Problems

### 1. Longest Palindrome
**File**: <a href="arrays/longest_palindrome.py" target="_blank">arrays/longest_palindrome.py</a>
- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Pattern**: Expand Around Center

### 2. Next Permutation
**File**: <a href="arrays/next_permutation.py" target="_blank">arrays/next_permutation.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Lexicographic Order

---

## 🗂️ Stack & Queue

### 1. Stack-based Questions
**File**: <a href="arrays/stack_based_question.py" target="_blank">arrays/stack_based_question.py</a>
- **Time Complexity**: Varies by problem
- **Space Complexity**: O(n)
- **Pattern**: Stack Data Structure Usage

---

## 🔍 Binary Search

### 1. Search Variations
**File**: <a href="arrays/two_sum_ii_and_iii_input_array_is_sorted.py" target="_blank">arrays/two_sum_ii_and_iii_input_array_is_sorted.py</a>
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(1)
- **Pattern**: Binary Search with Two Pointers

---

## 💰 Greedy Algorithms

### 1. Stock Problems
**File**: <a href="arrays/max_profit.py" target="_blank">arrays/max_profit.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Buy Low, Sell High

**File**: <a href="arrays/all_types_stock_question/max_profit.py" target="_blank">arrays/all_types_stock_question/max_profit.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Multiple Transaction Strategy

### 2. Job Scheduling
**File**: <a href="arrays/job_scheduling.py" target="_blank">arrays/job_scheduling.py</a>
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Pattern**: Greedy with Sorting

### 3. Meeting Overlap
**File**: <a href="arrays/metting_overlap_prob.py" target="_blank">arrays/metting_overlap_prob.py</a>
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(1)
- **Pattern**: Sort and Check Adjacent

---

## 🧮 Mathematical Problems

### 1. Factorial
**File**: <a href="arrays/factorial_program.py" target="_blank">arrays/factorial_program.py</a>
- **Time Complexity**: O(n)
- **Space Complexity**: O(n) for recursive, O(1) for iterative
- **Pattern**: Mathematical Computation

### 2. Happy Number
**File**: <a href="arrays/find_happy_number.py" target="_blank">arrays/find_happy_number.py</a>
- **Time Complexity**: O(log n)
- **Space Complexity**: O(log n)
- **Pattern**: Cycle Detection in Number Sequence

### 3. Pascal's Triangle
**File**: <a href="arrays/pascals_triangle.py" target="_blank">arrays/pascals_triangle.py</a>
- **Time Complexity**: O(n²)
- **Space Complexity**: O(n²)
- **Pattern**: Mathematical Pattern Generation

---

## 🔄 Concurrency

### 1. Concurrency Problems
**File**: <a href="arrays/concurrency/concurrency.py" target="_blank">arrays/concurrency/concurrency.py</a>
- **Time Complexity**: Varies by problem
- **Space Complexity**: Varies by problem
- **Pattern**: Thread Safety and Synchronization

---

## 📝 Summary Statistics

- **Total Problems**: 50+
- **Patterns Covered**: 15+
- **Data Structures**: Arrays, Trees, Graphs, Linked Lists, Stacks, Queues
- **Algorithms**: DP, Greedy, Two Pointers, Sliding Window, BFS/DFS
- **Language**: Primarily Python with some Go examples

---

## 🎯 How to Use This Guide

1. **Pattern-First Approach**: Start with a pattern you want to master
2. **Complexity Analysis**: Understand time/space trade-offs
3. **Implementation Practice**: Run the code and modify it
4. **Problem Variations**: Try similar problems with the same pattern

---

## 📚 Additional Resources

- **Striver's SDE Sheet**: [Link](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)
- **Data Structure Notes**: [Link](https://github.com/kumarakshay2456/Data_Structure_Notes)

---

## 🐹 Go Programming

### 1. Hello World
**File**: <a href="GO/hello_word.go" target="_blank">GO/hello_word.go</a>
- **Time Complexity**: O(1)
- **Space Complexity**: O(1)
- **Pattern**: Basic Go Syntax and Structure

### 2. Book API Implementation
**File**: <a href="GO/book-api/main.go" target="_blank">GO/book-api/main.go</a>
- **Time Complexity**: O(1) for server startup
- **Space Complexity**: O(1)
- **Pattern**: HTTP Server Setup

**File**: <a href="GO/book-api/handlers.go" target="_blank">GO/book-api/handlers.go</a>
- **Time Complexity**: O(n) for CRUD operations
- **Space Complexity**: O(n) for data storage
- **Pattern**: HTTP Handler Functions

**File**: <a href="GO/book-api/model.go" target="_blank">GO/book-api/model.go</a>
- **Time Complexity**: O(1)
- **Space Complexity**: O(1)
- **Pattern**: Data Structure Definition

**File**: <a href="GO/book-api/go.mod" target="_blank">GO/book-api/go.mod</a>
- **Dependencies**: Go module configuration
- **Pattern**: Dependency Management

---

## 🚀 CRUD API Implementations

### 1. Django REST API
**Directory**: <a href="crud_api_implementation_django/ticketing/" target="_blank">crud_api_implementation_django/ticketing/</a>
- **Framework**: Django with REST Framework
- **Database**: SQLite
- **Pattern**: Model-View-Serializer Architecture

**Key Files**:
- **Models**: <a href="crud_api_implementation_django/ticketing/api/models.py" target="_blank">crud_api_implementation_django/ticketing/api/models.py</a>
- **Views**: <a href="crud_api_implementation_django/ticketing/api/views.py" target="_blank">crud_api_implementation_django/ticketing/api/views.py</a>
- **Serializers**: <a href="crud_api_implementation_django/ticketing/api/serializers.py" target="_blank">crud_api_implementation_django/ticketing/api/serializers.py</a>
- **URLs**: <a href="crud_api_implementation_django/ticketing/api/urls.py" target="_blank">crud_api_implementation_django/ticketing/api/urls.py</a>

### 2. FastAPI Implementation
**File**: <a href="crud_api_implementation_fastapi/events.py" target="_blank">crud_api_implementation_fastapi/events.py</a>
- **Framework**: FastAPI
- **Database**: In-memory (can be extended)
- **Pattern**: Modern Async API with Pydantic Models

**File**: <a href="crud_api_implementation_fastapi/README.md" target="_blank">crud_api_implementation_fastapi/README.md</a>
- **Documentation**: API usage and setup instructions
- **Pattern**: Project Documentation

---

## 📊 Queue Data Structure

### 1. Queue Implementation
**File**: <a href="Queue/readme.md" target="_blank">Queue/readme.md</a>
- **Content**: Comprehensive queue data structure documentation
- **Pattern**: Queue Theory and Implementation
- **Topics**: FIFO operations, circular queues, priority queues

---

## 📄 JSON Operations

### 1. JSON Examples and Operations
**File**: <a href="json/all_examples.py" target="_blank">json/all_examples.py</a>
- **Time Complexity**: O(n) for parsing, O(1) for access
- **Space Complexity**: O(n) for data storage
- **Pattern**: JSON Serialization/Deserialization
- **Topics**: JSON parsing, manipulation, validation

---

## 📝 Summary Statistics

- **Total Problems**: 60+
- **Patterns Covered**: 20+
- **Data Structures**: Arrays, Trees, Graphs, Linked Lists, Stacks, Queues
- **Algorithms**: DP, Greedy, Two Pointers, Sliding Window, BFS/DFS
- **Languages**: Python, Go
- **Frameworks**: Django, FastAPI
- **Additional Topics**: CRUD APIs, Concurrency, JSON Operations

---

## 🎯 How to Use This Guide

1. **Pattern-First Approach**: Start with a pattern you want to master
2. **Complexity Analysis**: Understand time/space trade-offs
3. **Implementation Practice**: Run the code and modify it
4. **Problem Variations**: Try similar problems with the same pattern
5. **Full-Stack Learning**: Explore both algorithmic problems and API implementations

---

## 📚 Additional Resources

- **Striver's SDE Sheet**: <a href="https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/" target="_blank">Link</a>
- **Data Structure Notes**: <a href="https://github.com/kumarakshay2456/Data_Structure_Notes" target="_blank">Link</a>

---

*This guide organizes all solved problems by pattern for systematic learning and interview preparation.*
