def squire_sum(number):
    sum = 0
    while number:
        mod = number % 10
        number = number // 10
        sum += mod*mod
    return sum

def is_number_happy(num):
    slow = squire_sum(num)
    fast = squire_sum(squire_sum(num))
    while fast and fast != 1:
        slow = squire_sum(slow)
        fast = squire_sum(squire_sum(fast))
        if slow == fast:
            break
    return True if fast == 1 else False

def get_duplicate_number(nums):
    slow = nums[0]
    fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow




if __name__ == '__main__':
    nums = [2,5,9,6,9,3,8,9,7,1]
    print(get_duplicate_number(nums))


