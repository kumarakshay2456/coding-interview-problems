from collections import defaultdict
def get_longest_substring(nums, k):
    start = 0
    sub_string_map = defaultdict(int)
    max_len = -9
    n = len(nums)
    for end in range(n):
        sub_string_map[nums[end]] += 1
        if nums[end] == 0 and nums[end] in sub_string_map:
            while sub_string_map[nums[end]] > k :
                if nums[start] == 0:
                    sub_string_map[0] -= 1
                start += 1
                print("start and end", start , end)
        
        max_len = max(max_len, end - start + 1)
    return max_len 


if __name__ == '__main__':
    nums = [0,0,0,1]
    k = 2
    print(get_longest_substring(nums, k))
