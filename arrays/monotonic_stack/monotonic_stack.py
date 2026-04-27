"""
Monotonic Stack Pattern

A stack that maintains elements in strictly increasing or decreasing order.
When a new element violates the order, elements are popped — and those pops
are exactly when we can answer "next greater / smaller" queries.

Time: O(n) — each element is pushed and popped at most once.
Space: O(n)

Covers:
  1. Next Greater Element I & II
  2. Daily Temperatures
  3. Largest Rectangle in Histogram
  4. Trapping Rain Water (stack approach)
  5. Remove K Digits (monotonic deque)
  6. Sum of Subarray Minimums
"""


# ── 1. Next Greater Element ───────────────────────────────────────────────────
# For each element, find the next element to its right that is greater.
# Return -1 if none exists.

def next_greater_element(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    stack = []   # stores indices; stack top = most recent unresolved index

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)

    return result


# ── 2. Next Greater Element II (circular array) ───────────────────────────────
# Same as above but the array is circular (wrap around once).

def next_greater_element_circular(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(2 * n):        # iterate twice to simulate circular
        while stack and nums[i % n] > nums[stack[-1]]:
            result[stack.pop()] = nums[i % n]
        if i < n:
            stack.append(i)

    return result


# ── 3. Daily Temperatures ─────────────────────────────────────────────────────
# For each day, how many days until a warmer temperature?
# Return 0 if no warmer day exists.

def daily_temperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    result = [0] * n
    stack = []   # stores indices

    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)

    return result


# ── 4. Largest Rectangle in Histogram ────────────────────────────────────────
# Find the area of the largest rectangle that can be formed in the histogram.
# Key insight: when a bar is shorter than stack top, the stack top bar's
# rectangle extends from the new left boundary to the current index.

def largest_rectangle_in_histogram(heights: list[int]) -> int:
    # Stack stores indices; heights on stack are in increasing order.
    # When we pop index idx, its rectangle spans from stack[-1]+1 to i-1.
    stack = []
    max_area = 0
    heights = heights + [0]   # sentinel flushes the stack at the end

    for i in range(len(heights)):
        while stack and heights[stack[-1]] > heights[i]:
            h = heights[stack.pop()]
            w = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, h * w)
        stack.append(i)

    return max_area


# ── 5. Trapping Rain Water (stack approach) ───────────────────────────────────
# Alternative to two-pointer: uses a monotonic decreasing stack.
# When we find a bar taller than top, we found a valley — compute trapped water.

def trap_rain_water(height: list[int]) -> int:
    stack = []
    water = 0

    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            if not stack:
                break
            left = stack[-1]
            width = i - left - 1
            bounded_height = min(height[left], h) - height[bottom]
            water += width * bounded_height
        stack.append(i)

    return water


# ── 6. Sum of Subarray Minimums ───────────────────────────────────────────────
# For every subarray, sum up its minimum element.
# For each element, find how many subarrays it is the minimum of using
# previous-smaller and next-smaller boundaries.
# Time: O(n)  Space: O(n)

def sum_subarray_minimums(arr: list[int]) -> int:
    MOD = 10**9 + 7
    n = len(arr)
    # left[i] = distance to previous smaller (or equal) element
    # right[i] = distance to next smaller element
    left = [0] * n
    right = [0] * n
    stack: list[int] = []

    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    return sum(arr[i] * left[i] * right[i] for i in range(n)) % MOD


# ── Tests ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("── Next Greater Element ──")
    print(next_greater_element([2, 1, 2, 4, 3]))      # [4, 2, 4, -1, -1]
    print(next_greater_element_circular([1, 2, 1]))    # [2, -1, 2]

    print("\n── Daily Temperatures ──")
    print(daily_temperatures([73,74,75,71,69,72,76,73]))  # [1,1,4,2,1,1,0,0]

    print("\n── Largest Rectangle in Histogram ──")
    print(largest_rectangle_in_histogram([2,1,5,6,2,3]))  # 10
    print(largest_rectangle_in_histogram([2,4]))           # 4

    print("\n── Trapping Rain Water ──")
    print(trap_rain_water([0,1,0,2,1,0,1,3,2,1,2,1]))   # 6

    print("\n── Sum of Subarray Minimums ──")
    print(sum_subarray_minimums([3,1,2,4]))   # 17
