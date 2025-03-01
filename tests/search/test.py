from Lab4.KMP_search import kmp, prefix_func
from Lab5.BM_search import bm
from Lab5.BM_search_with_suffix import bm_suffix
from naive import naive_find
from timer import timer_decorator


def run_tests():
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМОВ ПОИСКА ПОДСТРОК")
    print("=" * 50)

    # Тест 1: Префикс-функция
    ex_str2 = 'aabaabaaaabaabaaab'
    print("\n[Тест 1]: Демонстрация массива префикс функции KMP:")
    print('Строка: A A B A A B A A A A B A A B A A A B')
    print('Префик:', *prefix_func(ex_str2))

    # Оборачиваем вызовы функций декоратором timer_decorator при тестировании
    naive_timed = timer_decorator(naive_find)
    kmp_timed = timer_decorator(kmp)
    bm_timed = timer_decorator(bm)
    bm_suffix_timed = timer_decorator(bm_suffix)

    # Тест 2: Поиск в строке
    finding = 'ababa'
    print(f"\n[Тест 2]: В '{ex_str2}' ищем '{finding}':")
    print(f"Naive: {naive_timed(ex_str2, finding)}")
    print(f"KMP: {kmp_timed(ex_str2, finding)}")
    print(f"BM: {bm_timed(ex_str2, finding)}")
    print(f"BM_suffix: {bm_suffix_timed(ex_str2, finding)}")

    # Тест 3: Поиск в файле
    try:
        with open('test.txt', 'r', encoding="utf-8") as f:
            text = f.read()
            find_this = 'дуб'
            print(f"\n[Тест 3]: В 'test.txt' ищем '{find_this}':")
            print(f"Naive: {naive_timed(text, find_this)}")
            print(f"KMP: {kmp_timed(text, find_this)}")
            print(f"BM: {bm_timed(text, find_this)}")
            print(f"BM_suffix: {bm_suffix_timed(text, find_this)}")
    except FileNotFoundError:
        print("\n[Тест 3]: Файл 'test.txt' не найден. Пропускаем тест с файлом.")

    # Тест 4: Ещё один пример
    ex_str3 = 'abababacab'
    find_3 = 'babac'
    print(f"\n[Тест 4]: В '{ex_str3}' ищем '{find_3}':")
    print(f"Naive: {naive_timed(ex_str3, find_3)}")
    print(f"KMP: {kmp_timed(ex_str3, find_3)}")
    print(f"BM: {bm_timed(ex_str3, find_3)}")
    print(f"BM_suffix: {bm_suffix_timed(ex_str3, find_3)}")

    print("\n" + "=" * 50)
    print("СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМОВ")
    print("=" * 50)

    # Тест на производительность с длинной строкой
    long_text = "a" * 10000 + "b" * 100 + "a" * 10000
    pattern_simple = "abb"
    pattern_complex = "b" * 50 + "a"

    print(f"\n[Производительность 1]: Поиск '{pattern_simple}' в длинной строке:")
    naive_timed(long_text, pattern_simple)
    kmp_timed(long_text, pattern_simple)
    bm_timed(long_text, pattern_simple)
    bm_suffix_timed(long_text, pattern_simple)

    print(f"\n[Производительность 2]: Поиск '{pattern_complex}' в длинной строке:")
    naive_timed(long_text, pattern_complex)
    kmp_timed(long_text, pattern_complex)
    bm_timed(long_text, pattern_complex)
    print(f"BM_suffix: {bm_suffix_timed(ex_str3, find_3)}")


if __name__ == "__main__":
    run_tests()
