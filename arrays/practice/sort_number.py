def sort_nums(nums):
    start = 0
    mid = 0
    end = len(nums) - 1 
    while mid <= end:
        if nums[mid] == 0:
            temp = nums[mid]
            nums[mid] = nums[start]
            nums[start] = temp
            mid += 1
            start += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            temp = nums[end]
            nums[end] = nums[mid]
            nums[mid] = start
            mid += 1
            end -= 1 
    return nums          

if __name__ == "__main__":
    nums = [2,0,2,1,1,0]
    print("Sort the list -> ", sort_nums(nums))