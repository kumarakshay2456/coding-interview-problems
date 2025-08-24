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
**File**: [arrays/longest-substring-without-repeating-characters.py](arrays/longest-substring-without-repeating-characters.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(min(m, n)) where m is charset size
- **Pattern**: Sliding Window with Hash Set

### 2. Longest Subarray with Ones After Replacement
**File**: [arrays/longest_subarray_with_ones_after_replacement.py](arrays/longest_subarray_with_ones_after_replacement.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Sliding Window with Count

### 3. Minimum Size Subarray Sum
**File**: [arrays/minimum_size_subarray_sum.py](arrays/minimum_size_subarray_sum.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Sliding Window with Sum Tracking

### 4. Fruit Into Baskets
**File**: [arrays/fruit-into-baskets.py](arrays/fruit-into-baskets.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Sliding Window with Two Types

---

## 👆 Two Pointers

### 1. Container With Most Water
**File**: [arrays/container_with_most_water.py](arrays/container_with_most_water.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Two Pointers from Ends

### 2. Trapping Rain Water
**File**: [arrays/trapping_rain_water.py](arrays/trapping_rain_water.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Two Pointers with Height Tracking

### 3. Sort Colors (0, 1, 2)
**File**: [arrays/sort_0_1_2.py](arrays/sort_0_1_2.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Three Pointers (Dutch National Flag)

### 4. Squares of a Sorted Array
**File**: [arrays/squares_of_a_sorted_array.py](arrays/squares_of_a_sorted_array.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(n)
- **Pattern**: Two Pointers from Ends

---

## 🎯 Dynamic Programming

### 1. Climbing Stairs
**File**: [arrays/DP_Problems/climbing-stairs.py](arrays/DP_Problems/climbing-stairs.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Fibonacci Sequence DP

### 2. Coin Change
**File**: [arrays/DP_Problems/coin_change.py](arrays/DP_Problems/coin_change.py){:target="_blank"}
- **Time Complexity**: O(amount * len(coins))
- **Space Complexity**: O(amount)
- **Pattern**: Unbounded Knapsack

### 3. Coin Change II (Combinations)
**File**: [arrays/DP_Problems/coin_change_2.py](arrays/DP_Problems/coin_change_2.py){:target="_blank"}
- **Time Complexity**: O(amount * len(coins))
- **Space Complexity**: O(amount)
- **Pattern**: Unbounded Knapsack Combinations

### 4. House Robber
**File**: [arrays/DP_Problems/house-robber.py](arrays/DP_Problems/house-robber.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: State Machine DP

### 5. Jump Game I
**File**: [arrays/DP_Problems/jum_game_1.py](arrays/DP_Problems/jum_game_1.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Greedy with DP

### 6. Target Sum
**File**: [arrays/DP_Problems/target_sum_2.py](arrays/DP_Problems/target_sum_2.py){:target="_blank"}
- **Time Complexity**: O(n * sum)
- **Space Complexity**: O(n * sum)
- **Pattern**: Subset Sum with Target

---

## 🌳 Tree Traversals

### 1. Binary Search Tree Operations
**File**: [tree/bst.py](tree/bst.py){:target="_blank"}
- **Insert**: O(h) time, O(h) space (recursive)
- **Search**: O(h) time, O(h) space (recursive)
- **Min/Max**: O(h) time, O(1) space
- **Pattern**: BST Property Maintenance

### 2. Tree Traversals
**File**: [tree/traversals.py](tree/traversals.py){:target="_blank"}
- **Inorder**: O(n) time, O(h) space
- **Preorder**: O(n) time, O(h) space
- **Postorder**: O(n) time, O(h) space
- **Level Order**: O(n) time, O(w) space
- **Pattern**: Recursive and Iterative Approaches

### 3. Level Order Traversal
**File**: [tree/level_order_traversal.py](tree/level_order_traversal.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(w) where w is max width
- **Pattern**: BFS with Level Tracking

### 4. Tree Properties
**File**: [tree/tree_are_identical.py](tree/tree_are_identical.py){:target="_blank"}
- **Time Complexity**: O(min(n1, n2))
- **Space Complexity**: O(min(h1, h2))
- **Pattern**: Recursive Comparison

### 5. Balance Tree Check
**File**: [tree/balance_tree.py](tree/balance_tree.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(h)
- **Pattern**: Height Balance Check

---

## 🔗 Linked List Operations

### 1. Basic Operations
**File**: [link_list/add_new_element.py](link_list/add_new_element.py){:target="_blank"}
- **Add**: O(n) time, O(1) space
- **Print**: O(n) time, O(1) space
- **Pattern**: Traversal and Modification

### 2. Reverse Operations
**File**: [link_list/reverse_ll.py](link_list/reverse_ll.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Three Pointer Technique

**File**: [link_list/reverse_in_group.py](link_list/reverse_in_group.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Group-wise Reversal

**File**: [link_list/reverse_ll_between_two_pointer.py](link_list/reverse_ll_between_two_pointer.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Partial List Reversal

### 3. Cycle Detection
**File**: [link_list/link_list_cycle.py](link_list/link_list_cycle.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Floyd's Cycle Finding

**File**: [link_list/link_list_cycle_2.py](link_list/link_list_cycle_2.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Cycle Start Detection

### 4. Middle Element
**File**: [link_list/find_middle_element.py](link_list/find_middle_element.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Fast and Slow Pointers

---

## 🕸️ Graph Algorithms

### 1. BFS and DFS
**File**: [graph/bfs_and_dfs.py](graph/bfs_and_dfs.py){:target="_blank"}
- **BFS**: O(V + E) time, O(V) space
- **DFS**: O(V + E) time, O(V) space
- **Pattern**: Graph Traversal Algorithms

### 2. Shortest Path
**File**: [graph/shortest_path.py](graph/shortest_path.py){:target="_blank"}
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Pattern**: BFS for Unweighted Graphs

**File**: [graph/shortest_path_v2.py](graph/shortest_path_v2.py){:target="_blank"}
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Pattern**: Enhanced BFS Implementation

### 3. Connected Components
**File**: [graph/count_component.py](graph/count_component.py){:target="_blank"}
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Pattern**: DFS Component Counting

---

## 📊 Array Manipulation

### 1. Kadane's Algorithm
**File**: [arrays/kadane_algo.py](arrays/kadane_algo.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Maximum Subarray Sum

### 2. Maximum Sum Subarray
**File**: [arrays/maximum_sum_sub_array.py](arrays/maximum_sum_sub_array.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Kadane's with Indices

### 3. Merge Operations
**File**: [arrays/merge_array.py](arrays/merge_array.py){:target="_blank"}
- **Time Complexity**: O(n + m)
- **Space Complexity**: O(n + m)
- **Pattern**: Two Sorted Arrays Merge

**File**: [arrays/merge_two_sorted_array.py](arrays/merge_two_sorted_array.py){:target="_blank"}
- **Time Complexity**: O(n + m)
- **Space Complexity**: O(1)
- **Pattern**: In-place Merge

### 4. Matrix Operations
**File**: [arrays/rotate_matrix.py](arrays/rotate_matrix.py){:target="_blank"}
- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Pattern**: Layer-wise Rotation

**File**: [arrays/set_matrix_zero.py](arrays/set_matrix_zero.py){:target="_blank"}
- **Time Complexity**: O(m * n)
- **Space Complexity**: O(1)
- **Pattern**: In-place Matrix Modification

### 5. Subarray Problems
**File**: [arrays/contiguous_sub_array_with_sum_k.py](arrays/contiguous_sub_array_with_sum_k.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(n)
- **Pattern**: Prefix Sum with Hash Map

**File**: [arrays/contiguous_array_equal_0_and_1.py](arrays/contiguous_array_equal_0_and_1.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(n)
- **Pattern**: Prefix Sum for Binary Arrays

---

## 🔤 String Problems

### 1. Longest Palindrome
**File**: [arrays/longest_palindrome.py](arrays/longest_palindrome.py){:target="_blank"}
- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Pattern**: Expand Around Center

### 2. Next Permutation
**File**: [arrays/next_permutation.py](arrays/next_permutation.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Lexicographic Order

---

## 🗂️ Stack & Queue

### 1. Stack-based Questions
**File**: [arrays/stack_based_question.py](arrays/stack_based_question.py){:target="_blank"}
- **Time Complexity**: Varies by problem
- **Space Complexity**: O(n)
- **Pattern**: Stack Data Structure Usage

---

## 🔍 Binary Search

### 1. Search Variations
**File**: [arrays/two_sum_ii_and_iii_input_array_is_sorted.py](arrays/two_sum_ii_and_iii_input_array_is_sorted.py){:target="_blank"}
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(1)
- **Pattern**: Binary Search with Two Pointers

---

## 💰 Greedy Algorithms

### 1. Stock Problems
**File**: [arrays/max_profit.py](arrays/max_profit.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Buy Low, Sell High

**File**: [arrays/all_types_stock_question/max_profit.py](arrays/all_types_stock_question/max_profit.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
- **Pattern**: Multiple Transaction Strategy

### 2. Job Scheduling
**File**: [arrays/job_scheduling.py](arrays/job_scheduling.py){:target="_blank"}
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Pattern**: Greedy with Sorting

### 3. Meeting Overlap
**File**: [arrays/metting_overlap_prob.py](arrays/metting_overlap_prob.py){:target="_blank"}
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(1)
- **Pattern**: Sort and Check Adjacent

---

## 🧮 Mathematical Problems

### 1. Factorial
**File**: [arrays/factorial_program.py](arrays/factorial_program.py){:target="_blank"}
- **Time Complexity**: O(n)
- **Space Complexity**: O(n) for recursive, O(1) for iterative
- **Pattern**: Mathematical Computation

### 2. Happy Number
**File**: [arrays/find_happy_number.py](arrays/find_happy_number.py){:target="_blank"}
- **Time Complexity**: O(log n)
- **Space Complexity**: O(log n)
- **Pattern**: Cycle Detection in Number Sequence

### 3. Pascal's Triangle
**File**: [arrays/pascals_triangle.py](arrays/pascals_triangle.py){:target="_blank"}
- **Time Complexity**: O(n²)
- **Space Complexity**: O(n²)
- **Pattern**: Mathematical Pattern Generation

---

## 🔄 Concurrency

### 1. Concurrency Problems
**File**: [arrays/concurrency/concurrency.py](arrays/concurrency/concurrency.py){:target="_blank"}
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
**File**: [GO/hello_word.go](GO/hello_word.go){:target="_blank"}
- **Time Complexity**: O(1)
- **Space Complexity**: O(1)
- **Pattern**: Basic Go Syntax and Structure

### 2. Book API Implementation
**File**: [GO/book-api/main.go](GO/book-api/main.go){:target="_blank"}
- **Time Complexity**: O(1) for server startup
- **Space Complexity**: O(1)
- **Pattern**: HTTP Server Setup

**File**: [GO/book-api/handlers.go](GO/book-api/handlers.go){:target="_blank"}
- **Time Complexity**: O(n) for CRUD operations
- **Space Complexity**: O(n) for data storage
- **Pattern**: HTTP Handler Functions

**File**: [GO/book-api/model.go](GO/book-api/model.go){:target="_blank"}
- **Time Complexity**: O(1)
- **Space Complexity**: O(1)
- **Pattern**: Data Structure Definition

**File**: [GO/book-api/go.mod](GO/book-api/go.mod){:target="_blank"}
- **Dependencies**: Go module configuration
- **Pattern**: Dependency Management

---

## 🚀 CRUD API Implementations

### 1. Django REST API
**Directory**: [crud_api_implementation_django/ticketing/](crud_api_implementation_django/ticketing/){:target="_blank"}
- **Framework**: Django with REST Framework
- **Database**: SQLite
- **Pattern**: Model-View-Serializer Architecture

**Key Files**:
- **Models**: [crud_api_implementation_django/ticketing/api/models.py](crud_api_implementation_django/ticketing/api/models.py){:target="_blank"}
- **Views**: [crud_api_implementation_django/ticketing/api/views.py](crud_api_implementation_django/ticketing/api/views.py){:target="_blank"}
- **Serializers**: [crud_api_implementation_django/ticketing/api/serializers.py](crud_api_implementation_django/ticketing/api/serializers.py){:target="_blank"}
- **URLs**: [crud_api_implementation_django/ticketing/api/urls.py](crud_api_implementation_django/ticketing/api/urls.py){:target="_blank"}

### 2. FastAPI Implementation
**File**: [crud_api_implementation_fastapi/events.py](crud_api_implementation_fastapi/events.py){:target="_blank"}
- **Framework**: FastAPI
- **Database**: In-memory (can be extended)
- **Pattern**: Modern Async API with Pydantic Models

**File**: [crud_api_implementation_fastapi/README.md](crud_api_implementation_fastapi/README.md){:target="_blank"}
- **Documentation**: API usage and setup instructions
- **Pattern**: Project Documentation

---

## 📊 Queue Data Structure

### 1. Queue Implementation
**File**: [Queue/readme.md](Queue/readme.md){:target="_blank"}
- **Content**: Comprehensive queue data structure documentation
- **Pattern**: Queue Theory and Implementation
- **Topics**: FIFO operations, circular queues, priority queues

---

## 📄 JSON Operations

### 1. JSON Examples and Operations
**File**: [json/all_examples.py](json/all_examples.py){:target="_blank"}
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

- **Striver's SDE Sheet**: [Link](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/){:target="_blank"}
- **Data Structure Notes**: [Link](https://github.com/kumarakshay2456/Data_Structure_Notes){:target="_blank"}

---

*This guide organizes all solved problems by pattern for systematic learning and interview preparation.*
