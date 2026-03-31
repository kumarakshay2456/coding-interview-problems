from typing import List

def subarraySum(nums: List[int], k: int) -> int:
    prefix_count = {0: 1}   # prefix_sum 0 occurs once (base case)
    prefix_sum = 0
    count = 0
    
    for num in nums:
        prefix_sum += num
        if prefix_sum - k in prefix_count:
            count += prefix_count[prefix_sum - k]
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1
    
    return count



if __name__ == '__main__':
    nums = [1,2,3]
    k = 3
    print("sub array count is ", subarraySum(nums,k))

