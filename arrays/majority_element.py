from typing import List

def majorityElement(nums: List[int]) -> int:
    freq_dict = {}
    total_len = len(nums)
    for i in nums:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    for key, value in freq_dict.items():
        if value >= total_len / 2:
            return key


print("majority element ->", majorityElement([3,2,3]))