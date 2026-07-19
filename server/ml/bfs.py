"""Breadth-first search — used for unweighted reachability checks (e.g. 'is this shelter reachable at all')."""
from collections import deque
from typing import Hashable, List

from ml.graph_algorithms import Graph


def bfs_path(graph: Graph, start: Hashable, goal: Hashable) -> List[Hashable]:
    if start == goal:
        return [start]

    visited = {start}
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]
        for neighbor, _weight in graph.neighbors(node):
            if neighbor in visited:
                continue
            new_path = path + [neighbor]
            if neighbor == goal:
                return new_path
            visited.add(neighbor)
            queue.append(new_path)

    return []
