def get_maximum_sum_sub_array(arr, k):
    n = len(arr)
    if k > n:
        return -1
    maximum_sum = arr[0] if k == 1 else 0
    pre_fix_sum = {0:arr[0]}
    for index in range(1, n):
        pre_fix_sum[index] = arr[index] + pre_fix_sum[index - 1]
        if index == (k - 1):
            maximum_sum = max(maximum_sum, pre_fix_sum[index])
        elif (index - k) in pre_fix_sum:
            k_sum = pre_fix_sum[index] - pre_fix_sum[index - k]
            maximum_sum = max(maximum_sum, k_sum)
    return maximum_sum

def get_maximum_sum_sub_array_sliding_window(nums, k):
    maximum_sum = 0
    window_sum = 0
    for i in range(k):
        window_sum = window_sum + nums[i]
    n = len(nums)
    maximum_sum = window_sum
    for i in range(k,n):
        window_sum = window_sum + nums[i] - nums[i-k]
        maximum_sum = max(maximum_sum, window_sum)
    return maximum_sum
        




if __name__ == '__main__':
    nums = [4, 2, 1, 7, 8, 1, 2, 8, 1, 0]
    k = 3
    print("Maximum Sum in sub array ", get_maximum_sum_sub_array(nums, k))
    print("Maximum Sum in sub array window ", get_maximum_sum_sub_array_sliding_window(nums, k))