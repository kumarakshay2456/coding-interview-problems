def get_two_sum_array(nums, target):
    start = 0
    end = len(nums) - 1
    while start < end:
        if (nums[start] + nums[end]) > target:
            end -= 1
        elif (nums[start] + nums[end]) == target:
            return [start+1, end+1]
        else:
            start += 1

        

if __name__ == '__main__':
    nums = [2,7,11,15]
    target = 26
    print(get_two_sum_array(nums, target))
