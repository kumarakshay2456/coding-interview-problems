from collections import Counter

def longestPalindrome(s: str) -> int:
    string_dict = Counter(s)
    max_palin = 0
    previous_max_odd_freq = 0
    for value in string_dict.values():
        if value % 2 == 0:
            max_palin += value
        else:
            if previous_max_odd_freq == 1:
                max_palin += value - 1
            else:
                max_palin += value
                previous_max_odd_freq = 1
    return max_palin


print("Value is -> ",longestPalindrome("bananas"))