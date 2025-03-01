from collections import deque
from enum import Enum
from math import atan2, degrees, hypot
from random import randint
from sys import maxsize

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')  # Используем стандартный бэкенд TkAgg


def graham_scan(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Pure implementation of graham scan algorithm in Python

    :param points: The unique points on coordinates.
    :return: The points on convex hell.

    """
    if len(points) <= 2:
        # There is no convex hull
        raise ValueError("graham_scan: argument must contain more than 3 points.")
    if len(points) == 3:
        return points
    # find the lowest and the most left point
    minidx = 0
    miny, minx = maxsize, maxsize
    for i, point in enumerate(points):
        x = point[0]
        y = point[1]
        if y < miny:
            miny, minx = y, x
            minidx = i
        if y == miny:
            if x < minx:
                minx = x
                minidx = i

    start_point = points[minidx]

    def angle_comparer(point: tuple[int, int]) -> float:
        """Return the angle toward to point from (minx, miny)

       :param point: The target point
              minx: The starting point's x
              miny: The starting point's y
       :return: the angle

       Examples:
       >>> angle_comparer((1,1), 0, 0)
       45.0

       >>> angle_comparer((100,1), 10, 10)
       -5.710593137499642

       """

        x = point[0]
        y = point[1]
        angle = degrees(atan2(y - start_point[1], x - start_point[0]))
        return angle

    def distance_comparer(point: tuple[int, int]) -> float:
        """Return the distance from the start point."""
        x = point[0]
        y = point[1]
        return hypot(x - start_point[0], y - start_point[1])

    sorted_points = sorted(points, key=lambda p: (angle_comparer(p), distance_comparer(p)))

    class Direction(Enum):
        left = 1
        straight = 2
        right = 3

    def cross_product(start: tuple[int, int], via: tuple[int, int], end: tuple[int, int]) -> int:
        """Return the cross product of vectors OA and OB."""
        return (via[0] - start[0]) * (end[1] - start[1]) - (via[1] - start[1]) * (end[0] - start[0])

    def check_direction(start: tuple[int, int], via: tuple[int, int], end: tuple[int, int]) -> Direction:
        """Determine the direction of movement from start to 'via' via end."""
        cross = cross_product(start, via, end)
        if cross > 0:
            return Direction.left
        elif cross < 0:
            return Direction.right
        else:
            return Direction.straight

    stack: deque[tuple[int, int]] = deque()  # doque for faster stack change at the ends
    [stack.append(sorted_points[i]) for i in range(0, 3)]
    # In any ways, the first 3 points line are towards left.
    # Because we sort them the angle from minx, miny.
    current_direction = Direction.left

    for i in range(3, len(sorted_points)):
        while len(stack) >= 2:
            start = stack[-2]
            via = stack[-1]
            end = sorted_points[i]
            if check_direction(start, via, end) != Direction.left:
                stack.pop()
            else:
                break
        stack.append(sorted_points[i])

    return list(stack)


def plot_points_and_hull(points: list[tuple[int, int]], hull: list[tuple[int, int]]):
    """Plot the points and the convex hull."""
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    hull_x = [point[0] for point in hull]
    hull_y = [point[1] for point in hull]

    plt.figure()
    plt.plot(x, y, 'o')  # Plot all points
    plt.plot(hull_x + [hull_x[0]], hull_y + [hull_y[0]], 'r-')  # Plot the convex hull
    plt.title("Graham Scan Convex Hull")
    plt.show()


if __name__ == "__main__":
    example_points = [(randint(0, 100), randint(0, 100)) for x in range(0, 50)]
    convex_hull = graham_scan(example_points)
    print(convex_hull)
    plot_points_and_hull(example_points, convex_hull)
