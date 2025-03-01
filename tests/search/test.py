from Lab4.KMP_search import kmp, prefix_func
from Lab5.BM_search import bm
from Lab5.BM_search_with_suffix import bm_suffix
from Lab6.RK_search import get_substring_rk
from naive import naive_find
from timer import timer_decorator


def run_search_test(test_label: str, text: str, pattern: str, algos: dict):
    """
    Функция для запуска теста поиска подстроки.
    Выводит заголовок теста, затем для каждого алгоритма – его название и результат.
    """
    text_display = text if len(text) <= 50 else text[:50] + "..."
    print(f"\n[{test_label}]: В '{text_display}' ищем '{pattern}':")
    for name, func in algos.items():
        result = func(text, pattern)
        print(f"{name}: {result}")


def run_tests():
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМОВ ПОИСКА ПОДСТРОК")
    print("=" * 50)

    # Тест 1: Префикс-функция KMP
    ex_str2 = 'aabaabaaaabaabaaab'
    print("\n[Тест 1]: Демонстрация массива префикс функции KMP:")
    print('Строка: A A B A A B A A A A B A A B A A A B')
    print('Префикс:', *prefix_func(ex_str2))

    # Оборачиваем алгоритмы в декоратор для измерения времени
    algorithms = {
        "Naive": timer_decorator(naive_find),
        "KMP": timer_decorator(kmp),
        "BM": timer_decorator(bm),
        "BM_suffix": timer_decorator(bm_suffix),
        "RK": timer_decorator(get_substring_rk),
    }

    # Тест 2: Поиск в строке ex_str2
    finding = 'ababa'
    run_search_test("Тест 2", ex_str2, finding, algorithms)

    # Тест 3: Поиск в файле
    try:
        with open('test.txt', 'r', encoding="utf-8") as f:
            file_text = f.read()
            find_this = 'дуб'
            run_search_test("Тест 3", file_text, find_this, algorithms)
    except FileNotFoundError:
        print("\n[Тест 3]: Файл 'test.txt' не найден. Пропускаем тест с файлом.")

    # Тест 4: Ещё один пример
    ex_str3 = 'abababacab'
    find_3 = 'babac'
    run_search_test("Тест 4", ex_str3, find_3, algorithms)

    print("\n" + "=" * 50)
    print("СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМОВ")
    print("=" * 50)

    # Тесты на производительность с длинной строкой
    long_text = "a" * 10000
    pattern_simple = "aaa"
    pattern_complex = "b" * 50 + "a"

    print(f"\n[Производительность 1]: Поиск '{pattern_simple}' в длинной строке:")
    for name, func in algorithms.items():
        result = func(long_text, pattern_simple)
        print(f"{name}: {result}")

    print(f"\n[Производительность 2]: Поиск '{pattern_complex}' в длинной строке:")
    for name, func in algorithms.items():
        result = func(long_text, pattern_complex)
        print(f"{name}: {result}")


if __name__ == "__main__":
    run_tests()
