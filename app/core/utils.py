from typing import List
from collections import defaultdict

def is_acyclic(nodes: List[str], edges: List[tuple[str, str]]) -> bool:
    graph = defaultdict(list)
    for src, dst in edges:
        graph[src].append(dst)

    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return False
        if node in visited:
            return True

        stack.add(node)
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        stack.remove(node)
        visited.add(node)
        return True

    for node in nodes:
        if node not in visited:
            if not dfs(node):
                return False
    return True
