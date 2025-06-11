def squire_sum(num:int):
    if num == 1:
        return 1
    else:
        temp_num = num
        squire_sum = 0
        while temp_num != 0:
            digit = temp_num % 10
            temp_num = temp_num // 10
            squire_sum = squire_sum + digit ** 2 if digit !=0 else squire_sum
    print("Squire Sum is", squire_sum)
    return squire_sum


def is_happy_number(num:int):
    if num == 1:
        return True
    else:
        sum_list = {}
        temp = num
        sqr_sum = squire_sum(num)
        while sqr_sum not in sum_list:
            if sqr_sum == 1:
                return True
            sum_list[sqr_sum] = temp
            temp = sqr_sum
            sqr_sum = squire_sum(sqr_sum)
        return False

# Using the fast and slow pointer
def is_happy_number_v2(num:int):
    if num == 1:
        return True
    slow = num
    fast = squire_sum(num)

    while fast != 1 and slow != fast:
        slow = squire_sum(slow)
        fast = squire_sum(squire_sum(fast))  # fast moves 2 steps

    return fast == 1
    

if __name__ == '__main__':
    """
    Approach 1: Using a Dictionary to Track Seen Numbers (Cycle Detection via Hashing)

    🔄 Logic
        •	Keep computing the square sum of digits.
        •	Use a dictionary or set to store previously seen results.
        •	If a result repeats → there’s a cycle → return False.
        •	If it becomes 1 → it’s a Happy Number.

    Approach 2: Fast and Slow Pointer (Floyd’s Cycle Detection)

    🐢🐇 Logic
        •	Similar to cycle detection in linked lists.
        •	Use two pointers:
        •	slow moves one step
        •	fast moves two steps
        •	If they meet at 1 → happy number.
        •	If they meet elsewhere → cycle → not a happy number.
    
    """
    print("SQUIRE NUMBER", is_happy_number(4))
        


