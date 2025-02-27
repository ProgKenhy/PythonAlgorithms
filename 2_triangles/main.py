import math
import numpy as np
import matplotlib.pyplot as plt
from functools import cmp_to_key
from matplotlib.patches import Polygon


def find_nested_triangles(points, visualize=False):
    """
    Проверяет, есть ли в наборе точек вложенные друг в друга треугольники,
    используя алгоритм Грэхема для построения выпуклых оболочек.

    Args:
        points: Список точек в формате [(x1, y1), (x2, y2), ...]
        visualize: Флаг для включения визуализации

    Returns:
        Булево значение, указывающее на наличие вложенных треугольников,
        и при visualize=True также найденные треугольники
    """
    if len(points) < 6:  # Нужно минимум 6 точек для двух треугольников
        return False, None, None if visualize else False

    # Функция для определения ориентации трех точек
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Коллинеарны
        return 1 if val > 0 else 2  # По часовой стрелке или против

    # Функция для проверки, находится ли точка внутри треугольника
    def is_point_inside_triangle(p, triangle):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        d1 = sign(p, triangle[0], triangle[1])
        d2 = sign(p, triangle[1], triangle[2])
        d3 = sign(p, triangle[2], triangle[0])

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    # Алгоритм Грэхема для построения выпуклой оболочки
    def graham_scan(points):
        if len(points) < 3:
            return points

        # Находим точку с минимальной y-координатой (самая нижняя точка)
        # При равных y-координатах, выбираем точку с минимальной x-координатой
        bottom_point = min(points, key=lambda p: (p[1], p[0]))

        # Функция для сортировки точек по полярному углу относительно bottom_point
        def polar_angle_comparator(p1, p2):
            o = orientation(bottom_point, p1, p2)
            if o == 0:  # Коллинеарны, выбираем ближайшую точку
                d1 = (p1[0] - bottom_point[0]) ** 2 + (p1[1] - bottom_point[1]) ** 2
                d2 = (p2[0] - bottom_point[0]) ** 2 + (p2[1] - bottom_point[1]) ** 2
                return -1 if d1 < d2 else 1
            return -1 if o == 2 else 1

        # Сортируем точки по полярному углу относительно bottom_point
        sorted_points = [bottom_point]
        sorted_points.extend(sorted(
            [p for p in points if p != bottom_point],
            key=cmp_to_key(polar_angle_comparator)
        ))

        # Построение выпуклой оболочки
        stack = [sorted_points[0], sorted_points[1]]

        for i in range(2, len(sorted_points)):
            while len(stack) > 1 and orientation(stack[-2], stack[-1], sorted_points[i]) != 2:
                stack.pop()
            stack.append(sorted_points[i])

        return stack

    # Получаем выпуклую оболочку всех точек
    convex_hull = graham_scan(points)

    # Если выпуклая оболочка имеет менее 3 точек, треугольников не будет
    if len(convex_hull) < 3:
        return False, None, None if visualize else False

    # Проверяем различные треугольники из выпуклой оболочки
    for i in range(len(convex_hull)):
        for j in range(i + 1, len(convex_hull)):
            for k in range(j + 1, len(convex_hull)):
                outer_triangle = [convex_hull[i], convex_hull[j], convex_hull[k]]

                # Создаем список точек, находящихся внутри внешнего треугольника
                points_inside = []
                for point in points:
                    if point not in outer_triangle and is_point_inside_triangle(point, outer_triangle):
                        points_inside.append(point)

                # Если внутри треугольника менее 3 точек, вложенного треугольника не будет
                if len(points_inside) < 3:
                    continue

                # Строим выпуклую оболочку для точек внутри треугольника
                inner_hull = graham_scan(points_inside)

                # Если можем построить треугольник из внутренних точек, значит есть вложенный треугольник
                if len(inner_hull) >= 3:
                    # Проверяем различные треугольники из внутренней выпуклой оболочки
                    for x in range(len(inner_hull)):
                        for y in range(x + 1, len(inner_hull)):
                            for z in range(y + 1, len(inner_hull)):
                                inner_triangle = [inner_hull[x], inner_hull[y], inner_hull[z]]
                                if visualize:
                                    return True, outer_triangle, inner_triangle
                                return True

    # Проверяем также точки, не входящие в выпуклую оболочку
    remaining_points = [p for p in points if p not in convex_hull]

    # Проходим по всем возможным треугольникам из оставшихся точек
    for i in range(len(remaining_points)):
        for j in range(i + 1, len(remaining_points)):
            for k in range(j + 1, len(remaining_points)):
                inner_triangle = [remaining_points[i], remaining_points[j], remaining_points[k]]

                # Проверяем, находится ли этот треугольник внутри какого-либо треугольника из выпуклой оболочки
                for x in range(len(convex_hull)):
                    for y in range(x + 1, len(convex_hull)):
                        for z in range(y + 1, len(convex_hull)):
                            outer_triangle = [convex_hull[x], convex_hull[y], convex_hull[z]]

                            # Проверяем, все ли точки внутреннего треугольника лежат внутри внешнего
                            if all(is_point_inside_triangle(p, outer_triangle) for p in inner_triangle):
                                if visualize:
                                    return True, outer_triangle, inner_triangle
                                return True

    return False, None, None if visualize else False


def visualize_nested_triangles(points):
    """
    Визуализирует набор точек и найденные вложенные треугольники, если они есть.

    Args:
        points: Список точек в формате [(x1, y1), (x2, y2), ...]
    """
    result, outer_triangle, inner_triangle = find_nested_triangles(points, visualize=True)

    # Создаем фигуру и оси
    fig, ax = plt.subplots(figsize=(10, 8))

    # Конвертируем точки в массивы numpy для удобства
    points_array = np.array(points)
    x, y = points_array[:, 0], points_array[:, 1]

    # Отображаем все точки
    ax.scatter(x, y, c='black', s=50, label='Все точки')

    # Если найдены вложенные треугольники, отображаем их
    if result:
        # Конвертируем треугольники в массивы numpy
        outer_tri = np.array(outer_triangle)
        inner_tri = np.array(inner_triangle)

        # Добавляем первую точку в конец для замыкания полигона
        outer_tri_closed = np.vstack([outer_tri, outer_tri[0]])
        inner_tri_closed = np.vstack([inner_tri, inner_tri[0]])

        # Отображаем внешний треугольник
        ax.plot(outer_tri_closed[:, 0], outer_tri_closed[:, 1], 'r-', lw=2, label='Внешний треугольник')
        ax.fill(outer_tri[:, 0], outer_tri[:, 1], 'r', alpha=0.2)

        # Отображаем внутренний треугольник
        ax.plot(inner_tri_closed[:, 0], inner_tri_closed[:, 1], 'b-', lw=2, label='Внутренний треугольник')
        ax.fill(inner_tri[:, 0], inner_tri[:, 1], 'b', alpha=0.4)

        # Отмечаем вершины треугольников
        ax.scatter(outer_tri[:, 0], outer_tri[:, 1], c='red', s=100, zorder=5, label='Вершины внешнего')
        ax.scatter(inner_tri[:, 0], inner_tri[:, 1], c='blue', s=100, zorder=5, label='Вершины внутреннего')

        plt.title('Найдены вложенные треугольники')
    else:
        plt.title('Вложенные треугольники не найдены')

    # Добавляем аннотации для всех точек
    for i, (xi, yi) in enumerate(points):
        ax.annotate(f"{i + 1}: ({xi}, {yi})", (xi, yi), xytext=(5, 5), textcoords="offset points")

    # Настройка графика
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True)
    ax.legend()

    # Равные масштабы осей
    ax.set_aspect('equal')

    # Сохраним результат в файл вместо прямого отображения
    plt.tight_layout()

    # Для PyCharm проблем с показом графиков можно использовать сохранение в файл
    # и обходной метод для отображения
    filename = "../4_KMP_search/nested_triangles_result.png"
    plt.savefig(filename)
    print(f"График сохранен в файл: {filename}")

    # А затем попробуем показать график, если это возможно
    try:
        plt.draw()
        plt.pause(0.001)  # Небольшая пауза для обновления GUI
    except Exception as e:
        print(f"Предупреждение: невозможно показать график интерактивно ({str(e)})")
        print(f"Просмотрите сохраненный файл: {filename}")

    return result


# Пример использования
if __name__ == "__main__":
    # Пример 1: Набор точек с вложенными треугольниками
    # points1 = [
    #     (0, 0), (10, 0), (5, 10),  # Внешний треугольник
    #     (3, 2), (7, 2), (5, 6)  # Внутренний треугольник
    # ]
    #
    # print("Пример 1:")
    # result1 = visualize_nested_triangles(points1)
    # print(f"Содержит вложенные треугольники: {result1}")
    #
    # # Пример 2: Набор точек без вложенных треугольников
    # points2 = [
    #     (0, 0), (10, 0), (5, 10),  # Треугольник
    #     (12, 8), (15, 10), (14, 5)  # Точки вне треугольника
    # ]
    #
    # print("\nПример 2:")
    # result2 = visualize_nested_triangles(points2)
    # print(f"Содержит вложенные треугольники: {result2}")

    # Пример 3: Случайный набор точек
    np.random.seed(42)  # Для воспроизводимости
    n_points = 20
    random_points = [(float(x), float(y)) for x, y in zip(
        np.random.randint(0, 100, n_points),
        np.random.randint(0, 100, n_points)
    )]

    print("\nПример 3 (случайные точки):")
    result3 = visualize_nested_triangles(random_points)
    print(f"Содержит вложенные треугольники: {result3}")
