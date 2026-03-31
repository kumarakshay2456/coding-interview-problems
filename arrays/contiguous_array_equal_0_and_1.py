nums = [0,1,1,1,1,1,0,0,0]
prefix_sum = 0
first_occurrence = {0: -1}
max_len = 0
for i , num in enumerate(nums):
    prefix_sum += 1 if num == 1 else -1
    print("prefix sum", prefix_sum)
    if prefix_sum in first_occurrence:
        max_len = max(max_len, i - first_occurrence[prefix_sum])
    else:
        first_occurrence[prefix_sum] = i
print("max length", max_len)

""""
Given a binary array nums, find the length of the longest contiguous subarray with equal number of 0s and 1s.

Soln - 
	•	It loops through a binary array nums of 0s and 1s.
	•	Maintains a prefix_sum, where:
	•	+1 for a 1
	•	-1 for a 0
	•	Uses a hashmap first_occurrence to store the first index where each prefix_sum appeared.
	•	If the same prefix_sum appears again at index i, it means the subarray between those two indices has equal number of 0s and 1s.
	•	It keeps track of the maximum such subarray length (max_len).

"""

