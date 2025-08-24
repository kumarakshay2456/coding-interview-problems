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



"""
Given a string s, return the length of the longest palindrome that can be built with the letters of s.

Letters are case-sensitive, so "Aa" is not the same as "aa"

Ex - s = "abccccdd"
Output - 7


Ex2 - s = "bananas"
Output - 5


"""
print("Value is -> ",longestPalindrome("bananas"))

def get_longest_palindrome(s)->int:
    string_dict = Counter(s)
    longest_palin = 0
    is_odd = False
    for value in string_dict.values():
        if value % 2 == 0:
            longest_palin += value
        else:
            longest_palin += (value - 1)
            is_odd = True
    return longest_palin + 1 if is_odd else longest_palin

print("Longest palindrome v2 -> ", get_longest_palindrome("abccccdd"))

