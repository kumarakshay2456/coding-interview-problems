#!/usr/bin/env node
/**
 * Generates docs/problems-detail.js (window.DSA_DETAIL_BY_ID) with statement + examples
 * for every problem id referenced in docs/index.html.
 */
import { readFileSync, writeFileSync } from 'fs';

/** Statement string + Example rows (spread). */
const def = (statement, ...examples) => ({
  statement,
  examples: examples.filter(Boolean),
});

const E = (input, output, explanation = '') => ({ input, output, explanation });

/* eslint-disable max-len — data file */
const D = {
  sw1: def(
    'Given an array of integers nums and positive integer k, return the maximum sum among all contiguous subarrays of length exactly k.',
    E('nums = [2, 1, 5, 1, 3, 2], k = 3', '9', 'Best window is [5,1,3] with sum 5+1+3=9.'),
    E('nums = [1], k = 1', '1', 'Single element.'),
  ),
  sw2: def(
    'Given a string s, find the length of the longest substring without repeating characters.',
    E('s = "abcabcbb"', '3', 'One longest substring without repeats is "abc" (same length alternatives like "bca", "cab" also reach 3); answer is length 3.'),
    E('s = "bbbbb"', '1', 'All repeats; longest unique substring length is 1.'),
    E('s = "pwwkew"', '3', '"wke" is valid with length 3 (not "pwke" — subsequence, not contiguous).'),
  ),
  sw3: def(
    'Given an array of positive integers nums and integer target, return the minimum length of a contiguous subarray whose sum is at least target. If none exists, return 0.',
    E('nums = [2,3,1,2,4,3], target = 7', '2', '[4,3] sums to 7.'),
    E('nums = [1,4,4], target = 4', '1', 'Single-element subarray.'),
  ),
  sw4: def(
    'You have a fruit tree orchard; each basket can hold unlimited fruit but only one type. You collect fruit with two baskets (at most two distinct types total). nums[i] is the type on tree i along a line. Find the longest contiguous sequence you can harvest under that rule.',
    E('fruits = [1,2,1]', '3', 'Types {1,2}: pick all three.'),
    E('fruits = [0,1,2,2]', '3', 'Best window is length 3 (e.g. [1,2,2]).'),
  ),
  sw5: def(
    'Given a binary array nums and integer k, return the longest contiguous subarray you can achieve if you may flip at most k zeros to ones.',
    E('nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2', '6', 'Flip zeros to lengthen the block of ones.'),
    E('nums = [0,0,1,1], k = 2', '4', 'You can flip two zeros.'),
  ),
  sw6: def(
    'Given integer array nums and integer k, return the number of contiguous subarrays whose sum equals k.',
    E('nums = [1,1,1], k = 2', '2', 'Subarrays starting at indices 0 and 1.'),
    E('nums = [1,2,3], k = 3', '2', '[3] and [1,2].'),
  ),
  sw7: def(
    'Given strings s and t, find the smallest window in s covering every character of t (with multiplicity). Return "" if impossible.',
    E('s = "ADOBECODEBANC", t = "ABC"', '"BANC"', 'Shortest contiguous substring covering A,B,C.'),
    E('s = "a", t = "a"', '"a"', 'Whole string.'),
  ),
  sw8: def(
    'Given strings s and p, return the starting indices in s of length-|p| substrings that are anagrams of p.',
    E('s = "cbaebabacd", p = "abc"', '[0, 6]', 'Windows "cba" and "bac".'),
    E('s = "abab", p = "ab"', '[0, 1, 2]', 'Every length-2 permutation of {"a","b"}.'),
  ),
  tp1: def(
    'Given n non-negative vertical lines at x = 1..n with heights height[i], pick two lines with x-axis forming a container. Return the largest area.',
    E('height = [1,8,6,2,5,4,8,3,7]', '49', 'Lines at index 1 and 8 (−1 semantics off-by-one avoided): area limited by shorter height.'),
    E('height = [1,1]', '1', 'Ends only.'),
  ),
  tp2: def(
    'Given non-negative elevations on a histogram, compute how much rainwater can be trapped.',
    E('height = [0,1,0,2,1,0,1,3,2,1,2,1]', '6', 'Standard valley fill.'),
    E('height = [4,2,0,3,2,5]', '9', 'Water pools between pillars.'),
  ),
  tp3: def(
    'Sort array nums containing only values 0, 1, and 2 in place (relative order optional unless specified). Classic Dutch National Flag.',
    E('nums = [2,0,2,1,1,0]', '[0,0,1,1,2,2]', 'Grouped by value.'),
    E('nums = [2,0,1]', '[0,1,2]', ''),
  ),
  tp4: def(
    'Given sorted array nums (possibly negative), return squared values sorted in ascending order.',
    E('nums = [-4,-1,0,3,10]', '[0,1,9,16,100]', 'Largest magnitudes squared last.'),
    E('nums = [-7,-3,2,3,11]', '[4,9,9,49,121]', ''),
  ),
  tp5: def(
    'Given integer nums, return triples [nums[i], nums[j], nums[k]] with distinct indices and sum 0. No duplicates in the triple list.',
    E('nums = [-1,0,1,2,-1,-4]', '[[−1,-1,2],[-1,0,1]]', 'Interpret minus sign as hyphen in output list notation.'),
    E('nums = [0,1,1]', '[]', ''),
    E('nums = [0,0,0]', '[[0,0,0]]', ''),
  ),
  tp6: def(
    'Given strictly increasing integers (1‑indexed answers) nums and target, return 1‑indexed pair (i,j) where nums[i−1]+nums[j−1]=target (guaranteed exactly one pair).',
    E('numbers = [2,7,11,15], target = 9', '[1, 2]', '2 + 7 = 9.'),
    E('numbers = [2,3,4], target = 6', '[1, 3]', ''),
  ),
  tp7: def(
    'Find shortest continuous subarray that, once sorted ascending, makes nums entirely sorted.',
    E('nums = [2,6,4,8,10,9,15]', '5', 'Must include range from first out‑of‑order through last.'),
    E('nums = [1,2,3,4]', '0', ''),
  ),
  fs1: def(
    'Return the middle node of a singly linked list. If even length, return the second middle.',
    E('head = [1,2,3,4,5]', 'node val 3', 'Slow/fast pointers stop at middle.'),
    E('head = [1,2,3,4,5,6]', 'node val 4', 'Second middle in even list.'),
  ),
  fs2: def(
    'Return true iff linked list has a cycle.',
    E('linked list enters cycle after some nodes', 'true | false', 'Classic Floyd.'),
    E('no cycle', 'false', ''),
  ),
  fs3: def(
    'Return the node where the cycle begins, or null if no cycle.',
    E('meet after loop', 'starts at duplication index', ''),
    E('straight list', 'null', ''),
  ),
  fs4: def(
    'Repeatedly replace number by sum of squared digits until 1 appears (happy) or a repeated value (cycle / not happy).',
    E('n = 19', 'true', '1²+9²=82 → … reaches 1.'),
    E('n = 2', 'false', 'Enters repeating cycle.'),
  ),
  fs5: def(
    'Given nums containing n+1 integers in range [1,n] inclusive, exactly one repeats. Find the duplicate using O(1) extra memory (Floyd-style on indices).',
    E('nums = [1,3,4,2,2]', '2', ''),
    E('nums = [3,1,3,4,2]', '3', ''),
  ),
  mi1: def(
    'Merge all overlapping intervals and return pairwise disjoint intervals.',
    E('intervals = [[1,3],[2,6],[8,10],[15,18]]', '[[1,6],[8,10],[15,18]]', ''),
    E('intervals = [[1,4],[4,5]]', '[[1,5]]', 'Touching counts as overlapping variant per problem wording.'),
  ),
  mi2: def(
    'Insert new interval into sorted non‑overlapping intervals and merge as needed.',
    E('intervals = [[1,3],[6,9]], new = [2,5]', '[[1,5],[6,9]]', ''),
    E('intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], new=[4,8]', '[[1,2],[3,10],[12,16]]', ''),
  ),
  mi3: def(
    'Given meeting intervals [start,end], compute minimum conference rooms.',
    E('intervals = [[0,30],[5,10],[15,20]]', '2', 'Overlap needs second room.'),
    E('intervals = [[7,10],[2,4]]', '1', ''),
  ),
  mi4: def(
    'Given sorted meetings, decide if anyone double‑books.',
    E('meetings overlapping', 'False', ''),
    E('meetings non‑overlapping', 'True', ''),
  ),
  mi5: def(
    'Given job intervals as [start, end] pairs, select the largest set of pairwise non‑overlapping jobs (typically sort by ending time — finish‑soonest greedy). Below: counts how many jobs can be taken.',
    E('jobs = [[1,4],[5,9],[11,13]]', '3', 'No overlaps — take all three.'),
    E('jobs = [[1,10],[5,14],[13,22]]', '2', 'Pick [1,10] then [13,22]; middle overlaps both.'),
  ),
  cy1: def(
    'Given nums permutation of [0,n] missing one element, find it.',
    E('nums = [3,0,1]', '2', 'missing 2'),
    E('nums = [0,1]', '2', 'n inferred from length'),
  ),
  cy2: def(
    'Find duplicate integer in-place using cyclic‑sort intuition.',
    E('nums = [1,3,4,2,2]', '2', ''),
    E('nums = [3,1,3,4,2]', '3', ''),
  ),
  cy3: def(
    'Nums values in [1,n]; return all absent values in range.',
    E('nums = [4,3,2,7,8,2,3,1]', '[5,6]', 'Order varies by statement.'),
    E('nums = [1,1]', '[2]', 'assuming n=len'),
  ),
  cy4: def(
    'Smallest missing positive integer in original array modification allowed O(1) space.',
    E('nums = [1,2,0]', '3', ''),
    E('nums = [3,4,-1,1]', '2', ''),
  ),
  cy5: def(
    'Element appearing more than ⌊n/2⌋ times — Boyer–Moore majority.',
    E('nums = [3,2,3]', '3', ''),
    E('nums = [2,2,1,1,1,2,2]', '2', ''),
  ),
  ll1: def(
    'Reverse singly linked list and return new head.',
    E('head = [1,2,3,4,5]', '[5,4,3,2,1]', ''),
    E('head = [1,2]', '[2,1]', ''),
  ),
  ll2: def(
    'Reverse nodes in linked list in groups of k.',
    E('head = [1,2,3,4,5], k = 2', '[2,1,4,3,5]', 'Last incomplete group untouched.'),
    E('head = [1,2,3,4,5], k = 3', '[3,2,1,4,5]', ''),
  ),
  ll3: def(
    'Reverse nodes between positions m and n (1‑indexed).',
    E('head = [1,2,3,4,5], m = 2, n = 4', '[1,4,3,2,5]', ''),
    E('head = [5]', 'm=1,n=1', '[5]', ''),
  ),
  ll4: def(
    'Return true iff linked list reads same forwards and backwards (O(n) time, O(1) space typical).',
    E('head = [1,2,2,1]', 'true', ''),
    E('head = [1,2]', 'false', ''),
  ),
  ll5: def(
    'Rotate linked list right by k steps.',
    E('head = [1,2,3,4,5], k = 2', '[4,5,1,2,3]', ''),
    E('head = [0,1,2], k = 4', '[2,0,1]', 'mod length'),
  ),
  bfs1: def(
    'Return binary tree nodes level‑by‑left‑to‑right.',
    E('root = [3,9,20,null,null,15,7]', '[[3],[9,20],[15,7]]', 'LeetCode level-order serialization.'),
    E('root = [1]', '[[1]]', ''),
  ),
  bfs2: def(
    'Rotten oranges spread to fresh every minute; grid of 0/1/2. Return minimum minutes to rot all reachable fresh or −1.',
    E('grid = [[2,1,1],[1,1,0],[0,1,1]]', '4', ''),
    E('grid = [[2,1,1],[0,1,1],[1,0,1]]', '-1', 'Unreachable fresh orange.'),
  ),
  bfs3: def(
    'Shortest mutation steps from beginWord to endWord changing one letter each step via dict word list.',
    E('begin="hit", end="cog", list contains path', 'length of shortest ladder', ''),
    E('no transformation path exists', '0 | impossible flag per spec', ''),
  ),
  bfs4: def(
    'Given the root of a binary tree, return the depth of its shallowest leaf (LeetCode 111 convention: shortest path counted in nodes root → leaf — so a direct child leaf has depth 2).',
    E('root = [3,9,20,null,null,15,7]', '2', 'Leaf 9 is only one hop from root ⇒ minimum depth path has two nodes.'),
    E('root = [2,null,3,null,4]', '5', 'Right‑skew chain: each level adds one node until the leaf.'),
  ),
  dfs1: def(
    "Given m×n grid of '1' land and '0' water, count islands (connected 4‑way).",
    E('grid [...]', 'integer count', 'Flood fill each component once.'),
    E('"0"‑only grid', '0', ''),
  ),
  dfs2: def(
    'Directed acyclic graph (or general) enumerate all directed paths source→target.',
    E('DAG small', '[[0,1,...], ...]', ''),
    E('single edge', '[[0,1]]', ''),
  ),
  dfs3: def(
    'Can graph be 2‑colored? (binary undirected bipartite)',
    E('edges even cycle', 'true', ''),
    E('triangle', 'false', ''),
  ),
  dfs4: def(
    'Count paths tree root‑to‑leaf (or downward) summing exactly target (prefix-sum trick).',
    E('paths example', '# paths', ''),
    E('no qualifying paths', '0', ''),
  ),
  dfs5: def(
    'Given the root of a binary tree and targetSum, return true if there is a root‑to‑leaf path whose values sum to targetSum.',
    E('root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22', 'true', 'Path 5 → 4 → 11 → 2 sums to 22.'),
    E('root = [1,2,3], targetSum = 5', 'false', 'Paths to leaves sum to 3 and 4.'),
  ),
  th1: def(
    'Design a median finder: streams integers and median() returns the middle value after each insert.',
    E('MedianFinder(); addNum(1); addNum(2); findMedian()', '"1.5"', 'Median of two numbers.'),
    E('addNum(3); findMedian()', '"2"', 'Values {1,2,3}: median middle element.'),
  ),
  th2: def(
    'Return the sliding window median for nums with window length k.',
    E('nums = [1,3,-1,-5], k = 2', '[2.0, 1.0, -3.0]', 'Even windows average the two middles.'),
    E('nums = [1,4,2,7], k = 4', '[3.5]', ''),
  ),
  th3: def(
    'Kth largest in array.',
    E('nums = [3,2,1,5,6,4], k = 2', '5', ''),
    E('nums = [3,2,3,1,2,4,5,5,6], k = 4', '4', ''),
  ),
  sub1: def(
    'Return powerset of nums (possibly with duplicates skipped per problem statement).',
    E('nums = [1,2,3]', '[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]', ''),
    E('nums = [0]', '[[],[0]]', ''),
  ),
  sub2: def(
    'Combination sum: reuse candidates infinite times to hit target.',
    E('candidates = [2,3,7], target = 7', '[[7],[2,2,3]]', 'ordering typical ascending lists.'),
    E('candidates = [2], target = 1', '[]', ''),
  ),
  sub3: def(
    'All well‑formed parentheses with n pairs.',
    E('n = 3', '["((()))","(()())","(())()","()(())","()()()"]', ''),
    E('n = 1', '["()"]', ''),
  ),
  sub4: def(
    'All permutations of distinct nums.',
    E('nums = [1,2,3]', 'length 6 list', ''),
    E('nums = [0,1]', '[[0,1],[1,0]]', ''),
  ),
  sub5: def(
    'Partition string so every piece is palindrome; return all partitions.',
    E('s = "aab"', '[["a","a","b"],["aa","b"]]', ''),
    E('s = "a"', '[["a"]]', ''),
  ),
  mbs1: def(
    'Search target in rotated sorted ascending array unique elements.',
    E('nums = [4,5,6,7,0,1,2], target = 0', '4', 'Index of 0.'),
    E('nums = [4,5,6,7,0,1,2], target = 3', '-1', ''),
  ),
  mbs2: def(
    'Minimum element in rotated sorted array.',
    E('nums = [3,4,5,1,2]', '1', ''),
    E('nums = [4,5,6,7,0,1,2]', '0', ''),
  ),
  mbs3: def(
    'Mountain array strictly increases then decreases; find peak index.',
    E('arr = [0,1,0]', '1', ''),
    E('arr = [0,2,1,0]', '1', ''),
  ),
  mbs4: def(
    'Binary search insertion index sorted distinct nums.',
    E('nums = [1,3,5,6], target = 5', '2', ''),
    E('nums = [1,3,5,6], target = 2', '1', ''),
  ),
  bx1: def(
    'Every element twice except one; find unique via XOR.',
    E('nums = [2,2,1]', '1', ''),
    E('nums = [4,1,2,1,2]', '4', ''),
  ),
  bx2: def(
    'Missing one number [0,n] from permutation length n.',
    E('nums = [3,0,1]', '2', ''),
    E('nums = [0,1]', '2', ''),
  ),
  bx3: def(
    'Exactly two singletons appearing once; retrieve both.',
    E('nums = [1,2,1,3,2,5]', '[3,5]', 'order may vary'),
    E('nums = [-1,0]', '[-1,0]', ''),
  ),
  tk1: def(
    'Top k frequent elements.',
    E('nums = [1,1,1,2,2,3], k = 2', '[1,2]', ''),
    E('nums = [1], k = 1', '[1]', ''),
  ),
  tk2: def(
    'K closest points to origin (Euclidean squared).',
    E('points = [[1,3],[-2,2]], k = 1', '[[-2,2]]', ''),
    E('points = [[3,3],[5,-1],[-2,4]], k = 2', '[[3,3],[-2,4]]', 'order flexible'),
  ),
  tk3: def(
    'Sliding window maximum for every window size k.',
    E('nums = [1,3,-1,-3,5,3,6,7], k = 3', '[3,3,5,5,6,7]', ''),
    E('nums = [1], k = 1', '[1]', ''),
  ),
  tk4: def(
    'Kth-largest stream: persist class that adds integers and exposes k‑th largest (LeetCode 703 style).',
    E('Construct k=3, add [4,5,8,2]; largest()', '8', ''),
    E('add(9); largest()', '8', ''),
  ),
  kw1: def(
    'Merge k sorted linked lists into one sorted list.',
    E('lists = [[1,4,5],[1,3,4],[2,6]]', '[1,1,2,3,4,4,5,6]', ''),
    E('lists = []', '[]', ''),
  ),
  kw2: def(
    'Find k pairs with smallest sums nums1[i] + nums2[j] (reuse indices independently).',
    E('nums1 = [1,7,11], nums2 = [2,4,6], k = 3', '[[1,2],[1,4],[1,6]]', ''),
    E('nums1 = [1,1,2], nums2 = [1,2,3], k = 4', '[[1,1],[1,2],[2,1],[1,3]]', 'ordering may vary with ties.'),
  ),
  kw3: def(
    'Matrix rows and cols sorted ascending; find k‑th smallest element.',
    E('matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8', '13', 'Count elements ≤ median via binary answer search.'),
    E('matrix = [[1,2],[1,3]], k = 2', '1', ''),
  ),
  ts1: def(
    'Can finish all courses with prerequisite pairs (cycle detection topological).',
    E('numCourses=2, prereq=[[1,0]]', 'true', ''),
    E('numCourses=2, prereq=[[1,0],[0,1]]', 'false', ''),
  ),
  ts2: def(
    'Return valid topological order courses or empty if impossible.',
    E('ordering exists', '[...]', ''),
    E('cycle exists', '[]', ''),
  ),
  ts3: def(
    'Derive alien dictionary character order consistency.',
    E('sorted words implying order', 'Lex string or contradiction', ''),
    E('invalid prefixes', '"", impossible', ''),
  ),
  ts4: def(
    'For an undirected tree of n nodes labeled 0…n−1 with edges array, output centroid IDs that minimize resultant forest height.',
    E('edges = [[1,0],[1,2],[2,4],[5,7],[7,10]], n = … (canonical LC 310 family)', '[1]', 'Peel leaves iterative pruning.'),
    E('star rooted at hub 0 touching 1–3 via degree 4', '[0]', ''),
  ),
  kn1: def(
    '0/1 knapsack: maximize total value without exceeding knapsack weight W.',
    E('capacity W = 7, wt = [1,3,4], values = [1,4,5]', '9', 'Pick wt 3+4 for value 9.'),
    E('W = 2, wt = [1,3], vals = [10,20]', '10', ''),
  ),
  kn2: def(
    'Given nonnegative nums and target sum T, decide whether some subset sums to T.',
    E('nums = [1,5,11,5], target = 11', 'true', 'Subset {11} works.'),
    E('nums = [1,2,5], target = 4', 'false', ''),
  ),
  kn3: def(
    'Partition multiset into two equal-sum subsets iff total sum even and subset sum total/2 is achievable.',
    E('nums = [1,5,11,5]', 'true', 'Each side totals 22/2.'),
    E('nums = [1,2,3,5]', 'false', 'Total sum is odd.'),
  ),
  kn4: def(
    'Count ways assign + or − in front of each array element so the overall sum equals target.',
    E('nums = [1], target = 1', '1', ''),
    E('nums = [1], target = 0', '0', ''),
  ),
  kn5: def(
    'Minimum coins (unbounded) to make amount—or −1.',
    E('coins=[1,2,5], amount=11', '3', '5+5+1'),
    E('coins=[2], amount=3', '-1', ''),
  ),
  kn6: def(
    'Max money robbing houses in a line cannot rob two adjacent.',
    E('nums=[2,7,9,3,1]', '12', ''),
    E('nums=[1,2,3,1]', '4', ''),
  ),
  fib1: def(
    'Ways to reach top stair taking 1 or 2 steps.',
    E('n = 3', '3', '1+1+1, 1+2, 2+1'),
    E('n = 5', '8', ''),
  ),
  fib2: def(
    'Can reach last index jumps nums[i]?',
    E('nums = [2,3,1,1,4]', 'true', ''),
    E('nums = [3,2,1,0,4]', 'false', ''),
  ),
  fib3: def(
    'Maximum subarray contiguous sum Kadane.',
    E('nums = [-2,1,-3,4,-1,2,1,-5,4]', '6', '[4,-1,2,1]'),
    E('nums = [1]', '1', ''),
  ),
  fib4: def(
    'First n rows Pascal triangle.',
    E('numRows = 5', '[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]', ''),
    E('numRows = 1', '[[1]]', ''),
  ),
  pd1: def(
    'Longest palindromic subsequence length.',
    E('bbbab', '4', ''),
    E('cbbd', '2', ''),
  ),
  pd2: def(
    'Longest palindromic substring.',
    E('babad', '"bab"|"aba"', ''),
    E('cbbd', 'bb', ''),
  ),
  pd3: def(
    'Count distinct palindrome substrings center expansion.',
    E('aaa', '6', ''),
    E('abc', '3', ''),
  ),
  pd4: def(
    'Minimum insertions needed to convert s into palindrome (mirror unmatched chars). Answer = length − LPS.',
    E('s = "zzazz"', '"0"', 'Already palindrome.'),
    E('s = "mbadm"', '"3"', ''),
  ),
  lcs1: def(
    'Longest Common Subsequence (not necessarily contiguous) of texts and return its length.',
    E('text1 = "abcde", text2 = "ace"', '"3"', 'Subsequence ace.'),
    E('text1 = "abc", text2 = "abc"', '"3"', ''),
  ),
  lcs2: def(
    'Minimum edits (insert, delete, replace) to convert word1 into word2 (Levenshtein distance).',
    E('horse, ros → 3 edits', '"3"', 'Replace chars / delete.'),
    E('word1="intention", word2="execution"', '"8"', ''),
  ),
  lcs3: def(
    'Longest common contiguous substring of two arrays/strings (must be uninterrupted). Return length.',
    E('nums1 = [1,2,5,15,6,7], nums2 = [0,17,17,17,17,17,17]', '2', '[6,7] aligns with substring length 2 of second list edge case.'),
    E('A = [0,1,2,6,7], B = [-1,-2,9,10,17,33,101]', '1', ''),
  ),
  lcs4: def(
    'Shortest string containing both strings as subsequences preserving order.',
    E('word1="ab", word2="acd"', '"acdbd"', ''),
    E('abc, cba', '"abcbac"', ''),
  ),
  tr1: def(
    'Given root of binary tree, return maximum depth (LeetCode: number of nodes along longest root-to-leaf path).',
    E('root = [3,9,20,null,null,15,7]', '"3"', 'Levels: 3 → 20 → leaf.'),
    E('root = [1,null,2]', '"2"', 'Skew depth two nodes.'),
  ),
  tr2: def(
    'Diameter = longest path between any two nodes (counts edges). DFS tracks local height + global longest.',
    E('root = [1,2,3,4,5]', '"3"', 'Path leaf4–leaf5 through root.'),
    E('root = [1,2]', '"1"', ''),
  ),
  tr3: def(
    'Maximum path gain in weighted tree edges can flip direction once at pivot (LC 124 style). Nodes may be negative — drop negative branches.',
    E('root = [-10,9,20,null,null,15,7]', '"42"', 'Best path picks 15+20+7 segment.'),
    E('root = [2,1]', '"3"', ''),
  ),
  tr4: def(
    'Return visible values from right side (last node encountered per depth in level order / right-first DFS).',
    E('root = [1,2,3,null,null,4]', '[1,3,4]', ''),
    E('root = [2,1]', '[2]', ''),
  ),
  tr5: def(
    'Validate BST: every descendant left subtree < node < descendants right subtree (strict inequalities sometimes relaxed).',
    E('root = [2,1,3]', 'true', ''),
    E('root = [5,1,4,null,null,3,6]', 'false', ''),
  ),
  tr6: def(
    'Return kth smallest value leveraging BST ordering (typically iterative in-order).',
    E('root containing 1…n, k=1', '(smallest value)', ''),
    E('same tree, k=3', '(third smallest)', ''),
  ),
  tr7: def(
    'Build tree from preorder and inorder traversals guaranteeing unique binary tree.',
    E('preorder=[3,9,20], inorder=[9,3,20]', 'root reconstructed', ''),
    E('single-node lists', '("one node tree")', ''),
  ),
  tr8: def(
    'Serialize/deserialize binary tree preserving structure (delimiter + null placeholders).',
    E('serialization of [1,2,3]', 'string/stream', ''),
    E('decoded stream', 'equal tree', ''),
  ),
  gph1: def(
    'Single-source shortest paths on nonnegative weighted directed graph.',
    E('edges = [(0→1:w=5),(0→2:w=10),(1→2:w=5)], src=0', 'dist=[0,5,10]', ''),
    E('disconnected reachable case', '("inf unreachable")', ''),
  ),
  gph2: def(
    'Network Delay Time: signal starts at node k spreading along directed edges weighted by latency; answer max shortest path or −1 unreachable.',
    E('edges=[[u,v,w]...], times, n,k per LC 743', '("max delay or -1")', ''),
    E('star graph instantaneous', '("max shortest")', ''),
  ),
  gph3: def(
    'Count connected components simple undirected graph via DSU.',
    E('n = 5, edges = [[0,1],[3,4]]', '"3"', ''),
    E('no edges five isolates', '"5"', ''),
  ),
  gph4: def(
    'Detect whether undirected graph has any cycle.',
    E('edges spanning tree extras', '("cycle true/false")', ''),
    E('tree-shaped', '("acyclic")', ''),
  ),
  gph5: def(
    'Redundant Undirected Connected Graph: drop last conflicting edge restoring tree.',
    E('edges=[[1,2],[2,3],[3,1]]', '[3,1]', ''),
    E('larger permutation', '(last offending edge)', ''),
  ),
  gph6: def(
    "Kruskal's algorithm builds MST greedily sorting edges ascending weight using DSU cycle checks.",
    E('small weighted graph', '("MST edges + total weight")', ''),
    E('already spanning tree duplicate edge', '("skip duplicates")', ''),
  ),
  ti1: def(
    'Implement trie with insert/word search/prefix check.',
    E('Trie(); insert(\"apple\")', 'startsWith(\"app\") → true',''),
    E('search(\"app\") → false prior insert', '(boolean)',''),
  ),
  ti2: def(
    'Dictionary matching with "." wildcard (try all children DFS).',
    E('Trie with words {\"cat\",\"mat\"}', 'wildcard ca. matches cat', ''),
    E('pattern lacks matches', '(false)', ''),
  ),
  ti3: def(
    'Count stored words extending a given prefix (frequency map DFS).',
    E('Trie with words {\"apple\",\"apricot\"}', 'prefix app → completions count depends on trie', ''),
    E('prefix zzz', '0', ''),
  ),
  ms1: def(
    'For nums1 ⊆ nums2, find next strictly greater element to the right inside nums2 (LeetCode 496).',
    E('nums1=[4,1,2], nums2=[1,3,4,2]', '[-1, 3, -1]', ''),
    E('nums1=[2,5], nums2=[8,48,92,209]', '[48,209]', ''),
  ),
  ms2: def(
    'For each temperature day, compute days waited until warmer (stack of indices monotone decreasing).',
    E('temperatures = [73,74,75,71,72,71,71,71]', '[1, 1, 0, 2, … per LC]', ''),
    E('temperatures=[30]', '[0]', ''),
  ),
  ms3: def(
    'Largest rectangular area trapped under histogram bars contiguous span.',
    E('height=[2,1,6,8,11]','classic area',''),
    E('uniform bars', '("max area")',''),
  ),
  ms4: def(
    'Sum over all contiguous subarrays of their minimum modulo 100000007 (contributions via prev/next lesser bounds).',
    E('[3,5,11]','weighted sum modulo',''),
    E('[1]', '("contribution = value")',''),
  ),
  lru1: def(
    'LRU eviction when capacity exceeded; get updates recency ordering.',
    E('capacity=2, put(1,1), put(2,2), get(1), put(3,3)', 'evicts least recent key among {1}', ''),
    E('capacity=3 sequence after mixed ops', 'final map state varies', ''),
  ),
  sys1: def(
    'Token bucket bursts to capacity refill rate r tokens/sec granting requests decrementing counters.',
    E('capacity=10 refill 1/sec, burst of 12 requests', 'later requests denied once bucket empties', ''),
    E('steady low rate steady demand', 'all succeed', ''),
  ),
  sys2: def(
    'Fixed sliding window timestamps deque dropping expired entries enforcing max RPM.',
    E('max 3 calls inside any 5s sliding window timestamps', '(track allow-or-deny per call)', ''),
    E('quiet period resets window', 'budget replenishes', ''),
  ),
  sys3: def(
    'Consistent hashing ring distributes keys to physical nodes with optional virtual replicas.',
    E('three servers placed on numeric ring clockwise successor lookup', '(returns physical node id)', ''),
    E('add fourth server reshuffles only neighboring segment', '(minimal key moves)', ''),
  ),
  gr1: def(
    'Minimum jumps reach end greedy farthest.',
    E('nums = [2,3,1,1,4]', '2', ''),
    E('nums = [2,3,0,1,4]', '2', ''),
  ),
  gr2: def(
    'Gas stations circuit clockwise if Σ(gas − cost) ≥ 0; find unique replenishing station else −1.',
    E('gas = [5,9,17], cost = [3,23,42]', '-1', 'Running tank never survives full lap.'),
    E('gas=[2,20], cost=[1,20]', '(start index LC134)', ''),
  ),
  gr3: def(
    'Erase minimum overlapping intervals Greedy ascending end-times (LC 426). Count removals enabling nonoverlap remainder.',
    E('intervals=[[3,16],[23,62],[82,93],[94,132],[133,173],[221,289]]','3',''),
    E('intervals=[[1,2],[5,17],[43,104]]','0',''),
  ),
  gr4: def(
    'Meetings chronological order feasibility if no pairwise overlap after sorting.',
    E('intervals=[[17,83],[73,178],[227,487]]','true',''),
    E('intervals intersect','false',''),
  ),
  gr5: def(
    'Partition greedy when scan index equals farthest occurrence of chars seen (LeetCode 763 pattern).',
    E('labels style string partitioning', '[partition lengths array]', ''),
    E('distinct letters never repeat later', '[full length]', ''),
  ),
  gr6: def(
    'CPU scheduling cool-down n separating identical frequent tasks heaps simulation.',
    E('tasks = "AAABBCCDD", cooldown = 7 slots', '(minimum schedule length)', ''),
    E('tasks = "A", cooldown = 0', '(length equals task count)', ''),
  ),
  mx1: def(
    'Spiral clockwise traversal inward boundary shrink.',
    E('matrix[[1,2,3],[4,5,6],[7,8,9]]','[1…9 spiral order]',''),
    E('single row[[1]]','[1]',''),
  ),
  mx2: def(
    'Rotate nxn clockwise 90° in place transpose + reverse.',
    E('matrix 3×3 incremental','rotated coords',''),
    E('identity','unchanged symmetry',''),
  ),
  mx3: def(
    'Mark rows/cols to zero exploiting first row/col as flags.',
    E('matrix zeros scatter','zeroed matrix',''),
    E('no zeros','same',''),
  ),
  mx4: def(
    'Binary-search flattened imaginary sorted matrix rows sorted.',
    E('matrix ascending rows/cols flattened search target=true','binary search',''),
    E('absent numbers','false',''),
  ),
  mx5: def(
    'Word search DFS backtracking board letters.',
    E('board = [["a","e"],["z","z"]]', 'word exits per adjacency DFS',''),
    E('word missing','false',''),
  ),
  st1: def(
    'Valid parentheses stacking.',
    E(' "()"', 'true', ''),
    E('"(]"', 'false', ''),
  ),
  st2: def(
    'Stack supporting push/pop/top retrieving current minimum amortized.',
    E('sequence push pop min sequence','tracked mins',''),
    E('duplicate mins','stack tuples',''),
  ),
  st3: def(
    'Evaluate Reverse Polish Notation integer stack arithmetic.',
    E('tokens = ["18","42","73","+", "-81", "*"]', '(evaluate int)',''),
    E('tokens = ["4","13","5","/","2"]','(fraction trunc toward zero LC 150)', ''),
  ),
  st4: def(
    'Decode repetitions nesting digits brackets.',
    E('s = \"3[z]2[y]\" expands pattern','decoded string multiplicative',''),
    E('nested 3[a2[c]] repeats substring acc three times', 'accaccacc', ''),
  ),
  st5: def(
    'Asteroid collisions positive move right negatives left stack simulation.',
    E('positions [5,-10]', 'positive destroyed',''),
    E('weights equal negate both','vanished',''),
  ),
  th4: def(
    'Median Finder follow-ups with streaming anomalies—same two heaps but document edge merges.',
    E('skewed pushes heavy tail','median stable',''),
    E('rapid duplicates','balancing rule',''),
  ),
  th5: def(
    'IPO greedy pick k projects respecting capital constraints heaps.',
    E('capital w projects heaps','max profit attainable',''),
    E('capital insufficient initially','delayed picks',''),
  ),
  kw4: def(
    'Smallest numeric range spanning all k sorted arrays simultaneously min-heap + max-track.',
    E('nums=[[44,48],[62,112],[131,289]]','tight sliding range',''),
    E('arrays length1 each','difference zero',''),
  ),
  ds1: def(
    'Min-stack variant storing tuples (value,min-so-far) enabling O(1) getMin.',
    E('push pop sequence','minimum queries',''),
    E('duplicate minimums stacked','handles ties',''),
  ),
  ds2: def(
    'Hash map design buckets chaining modulo prime resizing optional.',
    E('put get remove collisions','consistent semantics',''),
    E('rehash thresholds','migrate entries',''),
  ),
  ca1: def(
    'LRU cache identical constraints get/put O(1)',
    E('capacity=2 operations LRU','recent keys survive',''),
    E('over capacity eviction','drops LRU head',''),
  ),
  ca2: def(
    'LFU evicts lowest frequency LRU tiebreaker bucket structure.',
    E('fills capacity frequency ties','deterministic eviction',''),
    E('access increments freq migrating buckets','maintains invariant',''),
  ),
  ca3: def(
    'FIFO cache evicts eldest insertion irrespective of reads.',
    E('ordered inserts exceed capacity fifo','drop oldest insertion',''),
    E('hits do not reorder','contrasts LRU behavior',''),
  ),
  ca4: def(
    'Time-aware key/value sets with timestamped gets binary search retrieval.',
    E('multiple versions per timestamp','nearest previous value',''),
    E('nothing valid before deadline','fallback',''),
  ),
  ca5: def(
    'All O1 structure tracking counts inc dec min max via doubly-linked frequency buckets.',
    E('inc dec interplay','retrieve extremes',''),
    E('duplicate counts share nodes','unlink when zero',''),
  ),
  ca6: def(
    'Snapshot versioning array cells sparse map per index timeline.',
    E('snapshot index queries','bisect snaps',''),
    E('set after snapshot clones','immutable history',''),
  ),
  ca7: def(
    'Browser tabs history deque visit truncates forwards.',
    E('homepage visit back forward','pointer moves',''),
    E('visit clears redo stack','stateful pointer',''),
  ),
  ca8: def(
    'Streaming first unique FIFO skipping duplicates deque hash map combo.',
    E('add duplicates eventually unique front','polling',''),
    E('duplicate arrival drops older candidate','maintains uniqueness',''),
  ),
};



/* Ensure every numeric id discovered in repo index.html appears */
const INDEX = readFileSync(new URL('../docs/index.html', import.meta.url), 'utf8');
const probBlock =
  INDEX.slice(INDEX.indexOf('const PROBLEMS = ['), INDEX.indexOf('\n];\n\nconst PATTERNS')) || '';
const ids = [...probBlock.matchAll(/id:'([^']+)'/g)].map((m) => m[1]);
const uniq = [...new Set(ids)];

uniq.forEach((id) => {
  if (!D[id]) throw new Error(`Missing detail key: ${id}`);
});

Object.keys(D).forEach((k) => {
  if (!uniq.includes(k)) throw new Error(`Stray detail key not in PROBLEMS: ${k}`);
});

for (const v of Object.values(D)) {
  if (!Array.isArray(v.examples) || v.examples.length < 2) {
    throw new Error(`Need ≥2 examples: ${JSON.stringify(v).slice(0, 120)}`);
  }
}

for (const [id, o] of Object.entries(D)) {
  if (!String(o.statement || '').trim()) throw new Error(`Empty statement for ${id}`);
  o.examples.forEach((ex, i) => {
    if (!String(ex.input || '').trim()) throw new Error(`Empty example input ${id} #${i + 1}`);
    if (!String(ex.output || '').trim()) throw new Error(`Empty example output ${id} #${i + 1}`);
  });
}



const out =
  '// Auto-generated by scripts/build_problem_details.mjs — do not hand-edit.\nwindow.DSA_DETAIL_BY_ID=' +
  JSON.stringify(D, null, 2) +
  ';\n';
writeFileSync(new URL('../docs/problems-detail.js', import.meta.url), out);
console.error('Written docs/problems-detail.js with', uniq.length, 'problems');
