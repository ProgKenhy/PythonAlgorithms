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
