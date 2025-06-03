from collections import deque


class AhoCorasickNode:
    def __init__(self):
        self.children = {}  # Бор (префиксное дерево)
        self.fail = None  # Суффиксная ссылка
        self.output = []  # Шаблоны, оканчивающиеся в этой вершине


def build_aho_corasick(patterns):
    root = AhoCorasickNode()

    # Шаг 1: Построение бора
    for pattern in patterns:
        node = root
        for char in pattern:
            if char not in node.children:
                node.children[char] = AhoCorasickNode()
            node = node.children[char]
        node.output.append(pattern)

#         (root)
#       /   |   \
#      h    s    ...
#     / \    \
#    e   i    h
#   /    |     \
#  r     s      e
# /             |

    # Шаг 2: Построение суффиксных ссылок (BFS)
    queue = deque()
    root.fail = root
    for child in root.children.values():
        child.fail = root
        queue.append(child)

    while queue:
        current_node = queue.popleft()
        for char, child_node in current_node.children.items():
            # Ищем суффиксную ссылку для child_node
            fail_node = current_node.fail
            while fail_node != root and char not in fail_node.children:
                fail_node = fail_node.fail
            if char in fail_node.children:
                child_node.fail = fail_node.children[char]
            else:
                child_node.fail = root
            child_node.output += child_node.fail.output  # Наследуем output
            queue.append(child_node)

    return root


def search_aho_corasick(text, root):
    result = []
    current_node = root
    for i, char in enumerate(text):
        # Переход по failure links, если символ не найден
        while current_node != root and char not in current_node.children:
            current_node = current_node.fail
        if char in current_node.children:
            current_node = current_node.children[char]
        # Проверяем, есть ли совпадения
        for pattern in current_node.output:
            result.append((i - len(pattern) + 1, pattern))
    return result


patterns = ["he", "she", "his", "hers"]
root = build_aho_corasick(patterns)
text = "ushers"
print(search_aho_corasick(text, root))  # [(1, 'she'), (2, 'he'), (2, 'hers')]
