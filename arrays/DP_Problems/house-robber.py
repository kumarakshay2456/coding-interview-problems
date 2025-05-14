def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        curr = max(prev1, nums[i] + prev2)
        prev2 = prev1
        prev1 = curr
    
    return prev1

nums = [1,2,3,1]
print("Rob is", rob(nums))