def prefix_func(pattern: str) -> list:
    lps = [0] * len(pattern)
    prefix_len = 0
    i = 1

    for i in range(1, len(pattern)):
        while pattern[i] != pattern[prefix_len] and prefix_len > 0:
            prefix_len = lps[prefix_len - 1]

        if pattern[i] == pattern[prefix_len]:
            prefix_len += 1
            lps[i] = prefix_len
    return lps


def kmp(my_str: str, pattern:str) -> tuple[int, int]:
    lps = prefix_func(pattern)
    count = 0
    proverok = 0
    compare_index = 0
    for i in range(len(my_str)):
        while (compare_index > 0) and (my_str[i] != pattern[compare_index]):
            compare_index = lps[compare_index - 1]
            proverok += 1

        if my_str[i] == pattern[compare_index]:
            compare_index += 1
            proverok += 1

        if compare_index == len(pattern):
            proverok += 1
            count += 1
            compare_index = lps[len(pattern) - 1]
    return count, proverok



