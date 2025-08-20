def two_sum(arr, target_sum) -> (int, int):
    hash_map = {}
    for i, value in enumerate(arr):
        print("i ", i, value)
        complement = target_sum - value
        if complement in hash_map:
            return hash_map[complement], i
        hash_map[value] = i




if __name__ == '__main__':
    arr = [2,7,11,15]
    target_sum = 9
    print(f"Target sum is {two_sum(arr, target_sum)}")