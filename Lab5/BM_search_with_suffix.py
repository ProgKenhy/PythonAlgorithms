from Lab5.BM_search import get_bad_char_dict


def compute_suffix_table(pattern):
    """Создаёт таблицу суффиксов для эвристики хорошего суффикса"""
    m = len(pattern)
    suffix = [-1] * m

    # Обрабатываем случай, когда суффикс и префикс совпадают
    f = 0
    g = m - 1
    for i in range(m - 2, -1, -1):
        if i > g and suffix[i + m - 1 - f] < i - g:
            suffix[i] = suffix[i + m - 1 - f]
        else:
            if i < g:
                g = i
            f = i
            while g >= 0 and pattern[g] == pattern[g + m - 1 - f]:
                g -= 1
            suffix[i] = f - g

    return suffix


def compute_good_suffix_shift(pattern):
    """Вычисляет таблицу смещений для эвристики хорошего суффикса"""
    m = len(pattern)
    suffix = compute_suffix_table(pattern)

    # Таблица смещений на основе суффиксов
    shift = [0] * m

    # Заполняем случай 1 (нет подходящего суффикса)
    j = 0
    for i in range(m):
        shift[i] = m

    # Заполняем случай 2 (есть подходящий суффикс)
    for i in range(m - 1, -1, -1):
        if suffix[i] == i + 1:
            while j < m - 1 - i:
                if shift[j] == m:
                    shift[j] = m - 1 - i
                j += 1

    # Заполняем случай 3 (совпадение части суффикса)
    for i in range(0, m - 1):
        shift[m - 1 - suffix[i]] = m - 1 - i

    return shift


def bm_suffix(text: str, pattern: str, array_size: int = 256):
    """Реализация алгоритма Бойера-Мура с эвристикой плохого символа и хорошего суффикса"""
    if not pattern or not text:
        return 0, 0

    # Вычисляем таблицу смещений для эвристики плохого символа
    bad_char = get_bad_char_dict(pattern, array_size)

    # Вычисляем таблицу смещений для эвристики хорошего суффикса
    good_suffix = compute_good_suffix_shift(pattern)

    result = 0
    shift = 0
    comparisons = 0
    m = len(pattern)
    n = len(text)

    while shift <= (n - m):
        current_index = m - 1

        # Сравниваем символы паттерна с текстом справа налево
        while current_index >= 0 and pattern[current_index] == text[shift + current_index]:
            comparisons += 1
            current_index -= 1

        # Если current_index стал -1, значит нашли совпадение
        if current_index == -1:
            result += 1
            comparisons += 1

            # Смещаемся на основе эвристики хорошего суффикса для символа после паттерна
            shift += good_suffix[0]
        else:
            comparisons += 1

            # Вычисляем смещение по эвристике плохого символа
            char_code = ord(text[shift + current_index]) % array_size
            bad_char_shift = max(1, current_index - bad_char[char_code])

            # Вычисляем смещение по эвристике хорошего суффикса
            good_suffix_shift = good_suffix[current_index]

            # Используем максимальное из двух смещений
            shift += max(bad_char_shift, good_suffix_shift)

    return result, comparisons
