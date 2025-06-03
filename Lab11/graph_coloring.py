from typing import Dict, Optional, Tuple


def is_coloring_possible(graph: Dict[int, list], max_colors: int) -> Optional[Dict[int, int]]:
    """Проверяет, можно ли раскрасить граф в заданное количество цветов."""
    nodes = sorted(graph.keys(), key=lambda n: -len(graph[n]))
    assigned_colors = {}

    def dfs(node_idx: int) -> Optional[Dict[int, int]]:
        """Рекурсивно пытается раскрасить граф с помощью backtracking."""
        if node_idx == len(nodes):
            return assigned_colors.copy()

        current = nodes[node_idx]

        for color in range(1, max_colors + 1):
            if all(assigned_colors.get(neighbor) != color for neighbor in graph[current]):
                assigned_colors[current] = color
                result = dfs(node_idx + 1)
                if result is not None:
                    return result
                del assigned_colors[current]
        return None

    return dfs(0)


def minimum_colors(graph: Dict[int, list]) -> Tuple[int, Dict[int, int]]:
    """Находит минимальное количество цветов для раскраски графа."""
    max_degree = max(len(neighbors) for neighbors in graph.values())
    for colors in range(1, max_degree + 2):
        coloring = is_coloring_possible(graph, colors)
        if coloring:
            return colors, coloring
    return len(graph), {node: index + 1 for index, node in enumerate(graph)}


if __name__ == "__main__":
    examples = [
        {
            0: [2, 4],
            1: [3],
            2: [0, 3],
            3: [1, 2, 5],
            4: [0, 5],
            5: [3, 4]
        },
        {
            0: [1, 3],
            1: [0, 2, 4],
            2: [1, 5],
            3: [0, 4],
            4: [1, 3, 5],
            5: [2, 4]
        },
        {
            0: [1, 2, 3],
            1: [0, 4],
            2: [0, 5],
            3: [0, 6],
            4: [1, 7],
            5: [2, 7],
            6: [3, 7],
            7: [4, 5, 6]
        }
    ]

    for example_graph in examples:
        min_colors, color_assignment = minimum_colors(example_graph)
        print(f"Минимальное количество цветов: {min_colors}")
        print(f"Раскраска вершин: {color_assignment}")
        print()
