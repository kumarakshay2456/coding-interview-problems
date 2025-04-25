def longest_ones_subarray(arr, k):
    window_start = 0
    max_length = 0
    zero_count = 0

    for window_end in range(len(arr)):
        if arr[window_end] == 0:
            zero_count += 1

        while zero_count > k:
            if arr[window_start] == 0:
                zero_count -= 1
            window_start += 1

        max_length = max(max_length, window_end - window_start + 1)

    return max_length

if __name__ == '__main__':
    arr = [1, 1, 0, 0, 1, 1, 1, 0, 1]
    k = 2
    print(longest_ones_subarray(arr, k))
