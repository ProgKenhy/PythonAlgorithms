def naive_find(my_str: str, pattern:str) -> tuple[int, int]:
    count = 0
    proverok = 0
    for i in range(len(my_str) - len(pattern) + 1):
        flag = True
        for j in range(len(pattern)):
            proverok += 1
            if my_str[i + j] != pattern[j]:
                flag = False
                break
        if flag:
            count += 1
    return count, proverok


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


ex_str = 'ab sas abab safa ba ab sba ab ba'
ex_str2 = 'aabaabaaaabaabaaab'

finding = 'ababa'
print(naive_find(ex_str2, finding))


print('A A B A A B A A A A B A A B A A A B')
print(*prefix_func(ex_str2))
print(kmp(ex_str2, finding))

with open('test.txt', 'r', encoding="utf-8") as f:
    text = f.read()

    print(naive_find(text, 'дуб'))
    print(kmp(text, 'дуб'))


ex_str3 = 'abababacab'
find_3 = 'babac'
print('Наглядно')
print(naive_find(ex_str3, find_3))
print(kmp(ex_str3, find_3))
