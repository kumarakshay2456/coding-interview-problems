"""
You are given an integer array nums and an integer target.

You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer in nums 
and then concatenate all the integers.

For example, if nums = [2, 1], you can add a '+' before 2 and a '-' before 1 and concatenate them to build 
the expression "+2-1".

Return the number of different expressions that you can build, which evaluates to target.

Example 1:
    Input: nums = [1,1,1,1,1], target = 3
    Output: 5
    Explanation: There are 5 ways to assign symbols to make the sum of nums be target 3.
        -1 + 1 + 1 + 1 + 1 = 3
        +1 - 1 + 1 + 1 + 1 = 3
        +1 + 1 - 1 + 1 + 1 = 3
        +1 + 1 + 1 - 1 + 1 = 3
        +1 + 1 + 1 + 1 - 1 = 3

Example 2:
    Input: nums = [1], target = 1
    Output: 1
"""

def backtracking_sum(i, curr_sum, nums, target_sum, dp):
    """
    Recursive backtracking function with memoization to count the number of ways
    to reach the target sum by adding or subtracting nums[i] at each step.

    Args:
        i (int): current index in nums
        curr_sum (int): running sum so far
        nums (List[int]): input list of numbers
        target_sum (int): target value to achieve
        dp (dict): memoization dictionary to cache (i, curr_sum) results

    Returns:
        int: number of valid expressions that evaluate to target_sum
    """
    if i == len(nums):
        return 1 if curr_sum == target_sum else 0

    if (i, curr_sum) in dp:
        return dp[(i, curr_sum)]

    # Try both adding and subtracting the current number
    add = backtracking_sum(i + 1, curr_sum + nums[i], nums, target_sum, dp)
    subtract = backtracking_sum(i + 1, curr_sum - nums[i], nums, target_sum, dp)

    dp[(i, curr_sum)] = add + subtract
    return dp[(i, curr_sum)]


def get_target_sum(nums, target_sum):
    """
    Initializes the memoization table and starts the backtracking process.

    Args:
        nums (List[int]): input list of numbers
        target_sum (int): target value to achieve
    """
    dp = {}
    result = backtracking_sum(0, 0, nums, target_sum, dp)
    print("Number of ways to reach target:", result)


# Example usage
get_target_sum(nums=[1, 1, 1, 1, 1], target_sum=3)
get_target_sum(nums=[1], target_sum=1)