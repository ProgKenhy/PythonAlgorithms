from Lab4.KMP_search import kmp, prefix_func
from naive import naive_find

ex_str = 'ab sas abab safa ba ab sba ab ba'
ex_str2 = 'aabaabaaaabaabaaab'

finding = 'ababa'


print("Демонстрация массива префикс функции KMP:")
print('A A B A A B A A A A B A A B A A A B')
print(*prefix_func(ex_str2))
print(f"В '{ex_str2}' ищем '{finding}':")
print(f"Naive: {naive_find(ex_str2, finding)}")
print(f"KMP: {kmp(ex_str2, finding)}")

with open('test.txt', 'r', encoding="utf-8") as f:
    text = f.read()
    find_this = 'дуб'

    print(f"В 'test.txt' ищем '{find_this}':")
    print(f"Naive: {naive_find(text, find_this)}")
    print(f"KMP: {kmp(text, find_this)}")

ex_str3 = 'abababacab'
find_3 = 'babac'
print(f"В '{ex_str3}' ищем '{find_3}':")
print(f"Naive: {naive_find(ex_str3, find_3)}")
print(f"KMP: {kmp(ex_str3, find_3)}")
