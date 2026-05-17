def get_minimum_size_array(arr, target):
    min_len = float('inf')
    target_sum = 0
    start = 0
    for end in range(len(arr)):
        target_sum += arr[end]
        while target_sum >= target:
            min_len = min(min_len, end-start+1)
            target_sum = target_sum - arr[start]
            start += 1
    return min_len





if __name__ == '__main__':
    arr = [2,3,1,2,4,3]
    target = 7
    print(get_minimum_size_array(arr, target))
