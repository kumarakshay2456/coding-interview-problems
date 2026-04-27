"""
Given a string s, return the length of the longest palindrome that can be built with the letters of s.

Letters are case-sensitive, so "Aa" is not the same as "aa"

Ex - s = "abccccdd"
Output - 7


Ex2 - s = "bananas"
Output - 5

"""
from collections import Counter
def longest_palindrome(chars):
    data_dicts = Counter(chars)
    count = 0
    odd_counter = False
    for value in data_dicts.values():
        if value % 2 == 0:
            count += value
        else:
            count += value - 1 
            odd_counter = True
    
    return count + 1 if odd_counter else count

if __name__ == "__main__":
    chars = "bananas"
    print(longest_palindrome(chars))
