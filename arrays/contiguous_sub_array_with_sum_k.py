def subarraySum(nums, k):
    prefix_sum = 0
    count = 0
    freq = {0: 1}  # prefix sum 0 has appeared once

    for num in nums:
        prefix_sum += num

        # Check if (prefix_sum - k) has appeared before
        if prefix_sum - k in freq:
            count += freq[prefix_sum - k]

        # Update hashmap with current prefix_sum
        freq[prefix_sum] = freq.get(prefix_sum, 0) + 1

    return count

"""
Given an integer array nums and an integer k, return the total number of subarrays whose sum equals k.

Input: nums = [1, 2, 3], k = 3
Output: 2

Input: nums = [3, 4, 7, 2, -3, 1, 4, 2], k = 7
Output: 4

We use prefix sums just like in the contiguous array problem:

	•	Let prefix_sum[i] = sum of elements from nums[0..i].
	•	For each index i, we want to know if there exists a j < i such that:


    prefix_sum[i] - prefix_sum[j] = k


    That means the subarray (j+1 … i) has sum k.

    Rearranging:


    prefix_sum[j] = prefix_sum[i] - k


    So we can store counts of prefix sums in a hashmap.

    Think like this:

    “I’m at current sum = X
    Have I seen a previous sum = X - k?”

    If yes → 🎉 found a subarray

"""