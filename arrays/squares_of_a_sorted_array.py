def sort_squire_number(nums):
    start = 0
    end = len(nums) - 1
    sort_nums = [0] * len(nums)
    position = end
    while start <= end:
        if abs(nums[start]) > abs(nums[end]):
            sort_nums[position] = nums[start] ** 2
            start = start + 1
        else:
            sort_nums[position] = nums[end] ** 2
            end = end - 1
        position = position - 1
    print("Sort Number", sort_nums)

    return sort_nums


if __name__ == '__main__':
    """
    Given an integer array nums sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.
        Example 1:

        Input: nums = [-4,-1,0,3,10]
        Output: [0,1,9,16,100]
        Explanation: After squaring, the array becomes [16,1,0,9,100].
        After sorting, it becomes [0,1,9,16,100].

        Example 2:

        Input: nums = [-7,-3,2,3,11]
        Output: [4,9,9,49,121]
    
    """
    arr = [-4,-1,0,3,10]
    print(sort_squire_number(arr))
    arr = [-7,-3,2,3,11]
    print(sort_squire_number(arr))