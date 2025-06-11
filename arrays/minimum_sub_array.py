def min_subarray_with_k_unique(nums, k):
    freq = {}
    left = 0
    min_len = float('inf')
    unique_count = 0

    for right in range(len(nums)):
        num = nums[right]
        if num in freq:
            if freq[num] == 0:
                unique_count += 1
            freq[num] += 1
        else:
            freq[num] = 1
            unique_count += 1

        while unique_count >= k:
            min_len = min(min_len, right - left + 1)

            left_num = nums[left]
            freq[left_num] -= 1
            if freq[left_num] == 0:
                unique_count -= 1
            left += 1

    return min_len if min_len != float('inf') else -1


arr = [2,3,3,3,4,5,6,7]
k = 4

"""
Q - “Find the minimum length subarray that contains at least K unique numbers.”
Sol - 
To solve this type of problem, you usually:
	1.	Use two pointers: left and right to form a sliding window.
	2.	Use a dict or Counter to track the frequency of elements in the window.
	3.	Move the right pointer to expand the window.
	4.	Shrink the window from the left while maintaining at least k unique elements.
	5.	Track the minimum length of the valid window.

"""


print("minimum sum", min_subarray_with_k_unique(arr, k))