def minimum_size_of_sub_array(arr, target_sum):
    start = 0
    current_sum = 0
    minimum_length = 99999
    for end in range(len(arr)):
        current_sum += arr[end]
        while current_sum >= target_sum:
            minimum_length = min(minimum_length, end - start + 1)
            current_sum -= arr[start]
            start += 1
    return minimum_length if minimum_length != 99999 else 0

if __name__ == '__main__':
    
    """

    Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray
    whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.

    Example 1:

    Input: target = 7, nums = [2,3,1,2,4,3]
    Output: 2
    Explanation: The subarray [4,3] has the minimal length under the problem constraint.

    """
    target = 7
    nums = [2,3,1,2,4,3]
    print(minimum_size_of_sub_array(nums, target))
    target = 11
    nums = [1,1,1,1,1,1,1,1]
    print(minimum_size_of_sub_array(nums, 11))