def maximum_sub_array(arr, k):
    if k > len(arr):
        return "Subarray size k is greater than array length"
    
    # Initialize the first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    end_index = k - 1

    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        if window_sum > max_sum:
            max_sum = window_sum
            end_index = i
    
    # Extract the subarray
    max_subarray = arr[end_index - k + 1:end_index + 1]
    print("Maximum Subarray is:", max_subarray)
    print("Maximum Sum is:", max_sum)
    return max_subarray, max_sum


def longest_subarray_with_sum_k(arr, k):
    """
    Longest subarray with sum exactly equal to k
    """

    prefix_sum = 0
    max_len = 0
    prefix_map = {}

    for i in range(len(arr)):
        prefix_sum += arr[i]

        if prefix_sum == k:
            max_len = i + 1

        if (prefix_sum - k) in prefix_map:
            max_len = max(max_len, i - prefix_map[prefix_sum - k])

        if prefix_sum not in prefix_map:
            prefix_map[prefix_sum] = i

    return max_len

if __name__ == '__main__':
    """
    Maximum Sum Subarray of Size K:

    Description: Given an array of integers and a positive integer k, 
    find the maximum sum of any contiguous subarray of size k.
    """

    arr = [2,3,5,6,8,9,12,1,2,3,9]
    k = 3
    print(maximum_sub_array(arr, k))

    
    longest_subarray_with_sum_k()


