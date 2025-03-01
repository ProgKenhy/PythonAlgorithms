def get_bad_char_dict(pattern: str, array_size: int) -> list:
    """Создает таблицу смещений для эвристики плохого символа"""
    result = [-1] * array_size

    for i in range(len(pattern)):
        result[ord(pattern[i]) % array_size] = i

    return result


def bm(text: str, pattern: str, array_size: int = 256):
    """Реализация алгоритма Бойера-Мура с эвристикой плохого символа"""
    symbol_indexes = get_bad_char_dict(pattern, array_size)
    result = 0
    shift = 0
    comparisons = 0

    while shift < (len(text) - len(pattern)):
        current_index = len(pattern) - 1

        # Сравниваем символы паттерна с текстом справа налево
        while current_index >= 0 and pattern[current_index] == text[shift + current_index]:
            comparisons += 1
            current_index -= 1

        # Если current_index стал -1, значит нашли совпадение
        if current_index == -1:
            result += 1

            # Вычисляем смещение для следующего поиска
            if shift + len(pattern) < len(text):
                char_code = ord(text[shift + len(pattern)]) % array_size
                indent = len(pattern) - symbol_indexes[char_code]
            else:
                indent = 1

            shift += indent
        else:

            # Вычисляем смещение на основе эвристики плохого символа
            char_code = ord(text[shift + len(pattern)]) % array_size
            indent = symbol_indexes[char_code]

            shift += max(1, current_index - indent)

    return result, comparisons

# https://habr.com/ru/articles/660767/
