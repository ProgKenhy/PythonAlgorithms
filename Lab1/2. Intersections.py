import math

import matplotlib

matplotlib.use('Qt5Agg')


def intersection_two_lines(p1, p2, p3, p4):
    """
    Находит пересечение двух прямых, заданных точками (p1, p2) и (p3, p4).
    Формулы:
        A1 = y2 - y1
        B1 = x1 - x2
        C1 = x2*y1 - x1*y2
        Аналогично для второй прямой.
        Если определитель det = 0, то прямые параллельны или совпадают.
    Возвращает координаты точки пересечения или None.
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    A1 = y2 - y1
    B1 = x1 - x2
    C1 = x2 * y1 - x1 * y2

    A2 = y4 - y3
    B2 = x3 - x4
    C2 = x4 * y3 - x3 * y4

    det = A1 * B2 - A2 * B1
    if det == 0:
        return None
    x = (B1 * C2 - B2 * C1) / det
    y = (A2 * C1 - A1 * C2) / det
    return (x, y)


def intersection_line_segment(line_p1, line_p2, seg_p1, seg_p2):
    """
    Находит пересечение прямой, заданной (line_p1, line_p2), и отрезка (seg_p1, seg_p2).
    Проверяет, находится ли точка пересечения на отрезке.
    """
    line_int = intersection_two_lines(line_p1, line_p2, seg_p1, seg_p2)
    if not line_int:
        return None

    x, y = line_int
    x_min = min(seg_p1[0], seg_p2[0])
    x_max = max(seg_p1[0], seg_p2[0])
    y_min = min(seg_p1[1], seg_p2[1])
    y_max = max(seg_p1[1], seg_p2[1])

    if (x_min <= x <= x_max) and (y_min <= y <= y_max):
        return (x, y)
    return None


def intersection_two_segments(points: list):
    """
    Находит пересечение двух отрезков.
    Использует пересечение прямых и проверяет принадлежность точки пересечения каждому отрезку.
    """
    int_point = intersection_two_lines(points[0], points[1], points[2], points[3])
    if not int_point:
        return None

    x, y = int_point
    for seg in [(points[0], points[1]), (points[2], points[3])]:
        x_min = min(seg[0][0], seg[1][0])
        x_max = max(seg[0][0], seg[1][0])
        y_min = min(seg[0][1], seg[1][1])
        y_max = max(seg[0][1], seg[1][1])
        if not (x_min <= x <= x_max and y_min <= y <= y_max):
            return None
    return int_point


def intersection_line_circle(line_p1, line_p2, center, radius):
    """
    Находит пересечение прямой с окружностью.
    Формулы основаны на подстановке уравнения прямой в уравнение окружности.
    """
    x0, y0 = center
    x1, y1 = line_p1
    x2, y2 = line_p2

    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    a = A ** 2 + B ** 2
    b = 2 * (A * B * y0 - A * C - B ** 2 * x0)
    c = (C - B * y0) ** 2 + B ** 2 * (x0 ** 2 - radius ** 2)

    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return []

    points = []
    x = (-b + math.sqrt(discriminant)) / (2 * a)
    y = (-A * x - C) / B if B != 0 else (C + A * x) / B
    if discriminant == 0:
        points.append((x, y))
    else:
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        y2 = (-A * x2 - C) / B if B != 0 else (C + A * x2) / B
        points.extend([(x, y), (x2, y2)])
    return points


def intersection_segment_circle(seg_p1, seg_p2, center, radius):
    """
    Находит пересечение отрезка с окружностью.
    Использует пересечение прямой с окружностью и фильтрует точки, которые лежат на отрезке.
    """
    line_points = intersection_line_circle(seg_p1, seg_p2, center, radius)
    valid_points = []

    x_min = min(seg_p1[0], seg_p2[0])
    x_max = max(seg_p1[0], seg_p2[0])
    y_min = min(seg_p1[1], seg_p2[1])
    y_max = max(seg_p1[1], seg_p2[1])

    for p in line_points:
        if (x_min <= p[0] <= x_max) and (y_min <= p[1] <= y_max):
            valid_points.append(p)
    return valid_points


def intersection_two_circles(center1, radius1, center2, radius2):
    """
    Находит точки пересечения двух окружностей.
    Формулы основаны на геометрических соотношениях между центрами и радиусами.
    """
    x1, y1 = center1
    x2, y2 = center2
    d = math.hypot(x2 - x1, y2 - y1)

    if d > radius1 + radius2 or d < abs(radius1 - radius2):
        return []

    a = (radius1 ** 2 - radius2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(radius1 ** 2 - a ** 2)

    xm = x1 + a * (x2 - x1) / d
    ym = y1 + a * (y2 - y1) / d

    xs1 = xm + h * (y2 - y1) / d
    xs2 = xm - h * (y2 - y1) / d
    ys1 = ym - h * (x2 - x1) / d
    ys2 = ym + h * (x2 - x1) / d

    if xs1 == xs2 and ys1 == ys2:
        return [(xs1, ys1)]
    return [(xs1, ys1), (xs2, ys2)]


def plot_points_and_shapes(points, lines=False, segments=False, circles=None):
    """
    Plots the given points and geometric shapes for visualization.

    Args:
        points (list): List of points (x, y).
        lines (bool): Are lines there?
        segments (bool): Are segments there?
        circles (list): List of circles as tuples [(center, radius), ...].
    """
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots()

    # Plot points
    for i, (x, y) in enumerate(points):
        ax.plot(x, y, 'o', label=f'Point {i}')
        ax.text(x, y, f'{i + 1}', fontsize=12, ha='right')

    # Track limits for axis scaling
    x_min, x_max = float('inf'), float('-inf')
    y_min, y_max = float('inf'), float('-inf')

    if lines:
        k = len(points)-2 if segments else len(points)
        for i in range(0, k // 2 + 1, 2):
            x1, y1 = points[i][0], points[i][1]
            x2, y2 = points[i + 1][0], points[i + 1][1]

            if x2 - x1 != 0:  # Non-vertical line
                m = (y2 - y1) / (x2 - x1)
                b = y1 - m * x1
                x_vals = np.linspace(x1 - 10, x2 + 10, 400)
                y_vals = m * x_vals + b
            else:  # Vertical line
                x_vals = np.full(400, x1)
                y_vals = np.linspace(y1 - 10, y2 + 10, 400)

            ax.plot(x_vals, y_vals, '-k')
            x_min, x_max = min(x_min, x_vals.min()), max(x_max, x_vals.max())
            y_min, y_max = min(y_min, y_vals.min()), max(y_max, y_vals.max())


    if segments:
        for i in range(0, len(points) // 2 + 1, 2):
            x_vals = [points[i][0], points[i + 1][0]]
            y_vals = [points[i][1], points[i + 1][1]]
            ax.plot(x_vals, y_vals, '-k')
            x_min, x_max = min(x_min, *x_vals), max(x_max, *x_vals)
            y_min, y_max = min(y_min, *y_vals), max(y_max, *y_vals)


    if circles:
        for (center, radius) in circles:
            circle = plt.Circle(center, radius, color='blue', fill=False)
            ax.add_artist(circle)
            cx, cy = center
            x_min, x_max = min(x_min, cx - radius), max(x_max, cx + radius)
            y_min, y_max = min(y_min, cy - radius), max(y_max, cy + radius)

    # Adjust axis limits to include all shapes
    ax.set_xlim(x_min - 1, x_max + 1)
    ax.set_ylim(y_min - 1, y_max + 1)

    ax.set_aspect('equal', adjustable='datalim')
    plt.legend()
    plt.grid()
    plt.show()


def main_menu():
    while True:
        print("\nМеню операций:")
        print("1. Пересечение двух прямых")
        print("2. Пересечение прямой и отрезка")
        print("3. Пересечение двух отрезков")
        print("4. Пересечение прямой и окружности")
        print("5. Пересечение окружности и отрезка")
        print("6. Пересечение двух окружностей")
        print("7. Выход")

        choice = input("Выберите операцию: ")

        if choice == "1":
            print("Введите точки двух прямых:")
            # points = [list(map(float, input(f"Отрезок {j}, точка {i} (x y): ").split())) for i in range(1, 3) for j in
            #           range(1, 3)]
            points = [[1.0, 1.0], [1.0, 2.0], [2.0, 1.5], [1.2, 1.5]]
            result = intersection_two_lines(points[0], points[1], points[2], points[3])
            if result:
                print(f"Точка пересечения: {result}")
                plot_points_and_shapes(points, lines=True)
            else:
                print("Прямые параллельны или совпадают.")

        elif choice == "2":
            print("Введите точки прямой:")
            points = [list(map(float, input(("Прямая" if i < 2 else "Отрезок") + f" {j}, точка {i} (x y): ").split()))
                      for i in range(1, 3) for j in range(1, 3)]
            result = intersection_line_segment(points[0], points[1], points[2], points[3])
            if result:
                print(f"Точка пересечения: {result}")
                plot_points_and_shapes(points, segments=True, lines=True)
            else:
                print("Прямая и отрезок не пересекаются.")

        elif choice == "3":
            print("Введите точки двух отрезков:")
            # points = [list(map(float, input(f"Отрезок {j}, точка {i} (x y): ").split())) for i in range(1, 3) for j in
            #           range(1, 3)]
            points = [[1.0, 1.0], [2.0, 2.0], [2.0, 1.0], [1.0, 2.0]]
            result = intersection_two_segments(points)
            if result:
                print(f"Точка пересечения: {result}")
                plot_points_and_shapes(points, segments=True)
            else:
                print("Отрезки не пересекаются.")

        elif choice == "4":
            print("Введите точки прямой:")
            points = [list(map(float, input(f"Точка прямой {i} (x y): ").split())) for i in range(1, 3)]
            print("Введите центр окружности и радиус:")
            center = tuple(map(float, input("Центр (x y): ").split()))
            radius = float(input("Радиус: "))
            result = intersection_line_circle(points[0], points[1], center, radius)
            if result:
                print(f"Точки пересечения: {result}")
                plot_points_and_shapes(points, circles=[(center, radius)], lines=True)
            else:
                print("Прямая и окружность не пересекаются.")

        elif choice == "5":
            print("Введите точки отрезка:")
            points = [list(map(float, input(f"Точка отрезка {i} (x y): ").split())) for i in range(1, 3)]

            print("Введите центр окружности и радиус:")
            center = tuple(map(float, input("Центр (x y): ").split()))
            radius = float(input("Радиус: "))
            result = intersection_segment_circle(points[0], points[1], center, radius)
            if result:
                print(f"Точки пересечения: {result}")
                plot_points_and_shapes(points, circles=[(center, radius)], segments=True)
            else:
                print("Отрезок и окружность не пересекаются.")

        elif choice == "6":
            print("Введите данные первой окружности:")
            center1 = tuple(map(float, input("Центр (x y): ").split()))
            radius1 = float(input("Радиус: "))
            print("Введите данные второй окружности:")
            center2 = tuple(map(float, input("Центр (x y): ").split()))
            radius2 = float(input("Радиус: "))
            result = intersection_two_circles(center1, radius1, center2, radius2)
            if result:
                print(f"Точки пересечения: {result}")
                plot_points_and_shapes(points=[list(center1), list(center2)],
                                       circles=[(center1, radius1), (center2, radius2)])

            else:
                print("Окружности не пересекаются.")

        elif choice == "7":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

        # Основная программа


if __name__ == "__main__":
    main_menu()
