def get_three_sum_list(nums):
    res = []
    nums.sort()
    start = 0
    mid = 0
    end = len(nums) - 1
    while start < end:
        if nums[start] + nums[mid] + nums[end] == 0:
            res.append([nums[start], nums[mid], nums[end]])

        


if __name__ == '__main__':