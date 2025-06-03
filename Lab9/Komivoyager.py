from functools import lru_cache

input_matrix = [
    [0, 29, 82, 46, 68, 52, 72, 42, 51, 55, 99, 74, 23],
    [29, 0, 55, 46, 42, 43, 43, 23, 23, 31, 41, 51, 11],
    [82, 55, 0, 68, 46, 55, 23, 43, 41, 29, 79, 21, 64],
    [46, 46, 68, 0, 82, 15, 72, 31, 62, 42, 21, 51, 51],
    [68, 42, 46, 82, 0, 74, 23, 52, 21, 46, 82, 58, 46],
    [52, 43, 55, 15, 74, 0, 61, 23, 55, 31, 33, 37, 51],
    [72, 43, 23, 72, 23, 61, 0, 42, 23, 31, 77, 37, 51],
    [42, 23, 43, 31, 52, 23, 42, 0, 33, 15, 37, 33, 33],
    [51, 23, 41, 62, 21, 55, 23, 33, 0, 29, 62, 46, 29],
    [55, 31, 29, 42, 46, 31, 31, 15, 29, 0, 51, 21, 41],
    [99, 41, 79, 21, 82, 33, 77, 37, 62, 51, 0, 65, 42],
    [74, 51, 21, 51, 58, 37, 37, 33, 46, 21, 65, 0, 61],
    [23, 11, 64, 51, 46, 51, 51, 33, 29, 41, 42, 61, 0]
]


def tsp_dp(matrix):
    n = len(matrix)

    # Мемоизация: (текущий город, посещённые города) -> (мин. расстояние, путь)
    @lru_cache(maxsize=None)
    def dp(current, visited):
        if visited == (1 << n) - 1:  # Все города посещены
            return matrix[current][0], [0]  # Возвращаемся в стартовый город
        min_dist = 2 ** 31 - 1
        best_path = []
        for city in range(n):
            if not (visited & (1 << city)):  # Если город не посещён
                dist, path = dp(city, visited | (1 << city))
                total = matrix[current][city] + dist
                if total < min_dist:
                    min_dist = total
                    best_path = [city] + path
        return min_dist, best_path

    # Запуск из города 0
    total_dist, path = dp(0, 1 << 0)
    path = [0] + path  # Добавляем стартовый город в начало
    return total_dist, path


result = tsp_dp(input_matrix)
print('Минимальное расстояние:', result[0])
print('Оптимальный маршрут:', result[1])
