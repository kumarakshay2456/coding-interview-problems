"""
Given an array arr[] of size n, find the contiguous subarray (containing at least one number) which has the largest sum and return that sum.

arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]




"""

def maximum_sum_subarray(arr):
    curr_sum = arr[0]
    max_sum = arr[0]
    for i in range(1, len(arr)):
        curr_sum = max(arr[i], curr_sum + arr[i])
        max_sum = max(max_sum, curr_sum)
    return max_sum

arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print("Maximum sum of sub array",maximum_sum_subarray(arr))
