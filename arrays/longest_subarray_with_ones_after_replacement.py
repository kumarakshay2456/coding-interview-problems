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
    """
    You are given:
	•	A binary array arr (only contains 0s and 1s).
	•	An integer k — the maximum number of 0s you can flip to 1s.
        👉 You need to find the length of the longest subarray where you can flip at 
        most k zeros to 1s
    
    example - 
        arr = [1, 1, 0, 0, 1, 1, 1, 0]
        k = 2

    Concepet --- Contiguous?  --- Order Matters?  --- Example from [1, 2, 3]
    Subset---       NO         ---  NO            ----  [1, 3]
    Subsequence ---  NO          ---  Yes            ----  [1, 3]
    Subarray   ----   Yes        ---   Yes           ---- [1,2]
    """



    arr = [1, 1, 0, 0, 1, 1, 1, 0, 1]
    k = 2
    print(longest_ones_subarray(arr, k))
