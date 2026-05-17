def squares_nums(nums):
    result = [0]*len(nums)
    start = 0
    end = len(nums) - 1
    index = len(nums) - 1
    while start < end:
        if nums[start]*nums[start] < nums[end]*nums[end]:
            result[index] = nums[end]*nums[end]
            end -=  1
        else:
            result[index] = nums[start]*nums[start]
            start += 1
        index -= 1
    return result



if __name__ == '__main__':
    nums = [-4,-1,0,3,10]
    print(squares_nums(nums))