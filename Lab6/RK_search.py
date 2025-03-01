def get_substring_rk(text: str, pattern: str, base: int = 256, mod: int = 9973) -> int:
    n, m = len(text), len(pattern)
    if m == 0 or n < m:
        return 0

    result = 0
    pattern_hash = 0
    text_hash = 0
    first_index_hash = 1  # Коэффициент для старшего символа окна

    # Вычисляем first_index_hash = base^(m-1) mod mod
    for _ in range(m - 1):
        first_index_hash = (first_index_hash * base) % mod

    # Вычисляем начальные хеши для шаблона и первого окна текста
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        text_hash = (text_hash * base + ord(text[i])) % mod

    # Перебор окон текста
    for i in range(n - m + 1):
        # Если хеши совпадают, делаем посимвольное сравнение для проверки коллизии
        if pattern_hash == text_hash and text[i:i + m] == pattern:
            # result.append(i)
            result += 1

        # Если окно не последнее, обновляем хеш для следующего окна
        if i < n - m:
            # Вычитаем вклад старшего символа
            text_hash = (text_hash - ord(text[i]) * first_index_hash) % mod
            # Умножаем на base и добавляем следующий символ
            text_hash = (text_hash * base + ord(text[i + m])) % mod
            # Гарантируем, что значение хеша положительное
            text_hash %= mod

    return result
