def length_of_longest_substring(s: str) -> int:
    char_index = {}
    start = 0
    max_len = 0

    for end in range(len(s)):
        if s[end] in char_index and char_index[s[end]] >= start:
            start = char_index[s[end]] + 1  # skip the duplicate

        char_index[s[end]] = end  # update latest index of char
        max_len = max(max_len, end - start + 1)

    return max_len



            


if __name__ == '__main__':
    p = length_of_longest_substring('abcabcbb')
    print("Maximum Longest Substring is -> ", p )