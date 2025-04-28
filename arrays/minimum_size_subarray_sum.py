def find_minimum_subarray(arr, target):
    minimum_sum_sub_array_length = float('inf')
    start = 0
    current_sum = 0
    for end in range(len(arr)):
        current_sum += arr[end]
        while current_sum >= target:
            minimum_sum_sub_array_length = min(minimum_sum_sub_array_length, end - start + 1)
            current_sum -= arr[start]
            start += 1
    return minimum_sum_sub_array_length if minimum_sum_sub_array_length != float('inf') else 0






if __name__ == '__main__':

    """
    Given an array of positive integers nums and a positive integer target,
    return the minimal length of a whose sum is greater than or equal to target. 
    If there is no such subarray, return 0 instead.
    Example 1:
        Input: target = 7, nums = [2,3,1,2,4,3]
    
    Output: 2
        Explanation: The subarray [4,3] has the minimal length under the problem constraint.
    """
    arr = [2,3,1,2,4,3]
    target = 7
    print(find_minimum_subarray(arr, target))
    arr = [1,1,1,1,1,1,1,1]
    target = 11
    print(find_minimum_subarray(arr, target))


