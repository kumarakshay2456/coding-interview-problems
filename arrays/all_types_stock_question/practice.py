get_square_sum_cache = {}

def get_square_sum(n:int):
    if n in get_square_sum_cache:
        return get_square_sum_cache[n]
    if n == 1:
        return 1
    square_sum = 0
    temp = n
    while temp:
        digit = temp % 10
        temp = temp // 10
        square_sum += digit*digit
    get_square_sum_cache[n] = square_sum
    return square_sum


def is_number_is_happy(n:int):
    if n == 1:
        return True
    slow = n
    fast = get_square_sum(n)
    while fast != 1 and slow != fast:
        slow = get_square_sum(slow)
        fast = get_square_sum(get_square_sum(fast))
        print(f"slow {slow} and fast {fast}")
    return fast == 1



def main():
    num = 19
    print(is_number_is_happy(num))
if __name__ == "__main__":
    main()