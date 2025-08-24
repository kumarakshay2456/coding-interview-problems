nums = [0,1,1,1,1,1,0,0,0]
prefix_sum = 0
first_occurrence = {0: -1}
max_len = 0
for i , num in enumerate(nums):
    prefix_sum += 1 if num == 1 else -1
    print("prefix sum", prefix_sum)
    if prefix_sum in first_occurrence:
        max_len = max(max_len, i - first_occurrence[prefix_sum])
    else:
        first_occurrence[prefix_sum] = i
print("max length", max_len)

