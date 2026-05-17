def get_longest_substring_without_repeating(chars:str):
    start = 0
    end = 0
    hash_string = {}
    max_len = 0
    for end in range(len(chars)):
        if chars[end] in hash_string and hash_string[chars[end]] >= start:
            start = hash_string[chars[end]] + 1

        hash_string[chars[end]] = end
        max_len = max(max_len, end - start + 1)
    return max_len



if __name__ == '__main__':
    s = "abcabcbb"
    print(get_longest_substring_without_repeating(s))