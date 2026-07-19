"""Depth-first search — used for connected-component checks (e.g. is a region cut off by a disaster)."""
from typing import Hashable, Set

from ml.graph_algorithms import Graph


def dfs_reachable_set(graph: Graph, start: Hashable) -> Set[Hashable]:
    """Returns every node reachable from `start`."""
    visited: Set[Hashable] = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor, _weight in graph.neighbors(node):
            if neighbor not in visited:
                stack.append(neighbor)

    return visited
