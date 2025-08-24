"""
Given an array arr[] of size n, find the contiguous subarray (containing at least one number) which has the largest sum and return that sum.

arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

Soln - 
Scenario 1 - subarray sum (+ive) + current (+ive) -> Extend the sub array
Scenario 2 - subarray sum (-ive) + current (+ive) -> start New sub array
Scenario 3 - subarray sum (+ive) + current (-ive) -> Extend the sub array
Scenario 4 - subarray sum (-ive) + current (-ive) -> start New sub array

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


def maximum_sum_subarray(arr):
    curr_sum = arr[0]
    max_sum = arr[0]

    # Track indices
    start = end = s = 0

    for i in range(1, len(arr)):
        if arr[i] > curr_sum + arr[i]:
            curr_sum = arr[i]
            s = i   # new start
        else:
            curr_sum += arr[i]

        if curr_sum > max_sum:
            max_sum = curr_sum
            start = s
            end = i

    return max_sum, arr[start:end+1]


# Take input from the user
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

max_sum, subarray = maximum_sum_subarray(arr)
print("Maximum sum of subarray:", max_sum)
print("Subarray with maximum sum:", subarray)
