"""
Generic weighted-graph representation shared by the pathfinding algorithms
in this package (dijkstra, astar, bfs, dfs). Nodes are (lat, lng) tuples or
arbitrary hashable IDs; edges carry a distance-like weight.
"""
from collections import defaultdict
from typing import Dict, Hashable, List, Tuple


class Graph:
    def __init__(self):
        self.adjacency: Dict[Hashable, List[Tuple[Hashable, float]]] = defaultdict(list)

    def add_edge(self, u: Hashable, v: Hashable, weight: float, bidirectional: bool = True) -> None:
        self.adjacency[u].append((v, weight))
        if bidirectional:
            self.adjacency[v].append((u, weight))

    def neighbors(self, node: Hashable) -> List[Tuple[Hashable, float]]:
        return self.adjacency.get(node, [])

    def nodes(self) -> List[Hashable]:
        return list(self.adjacency.keys())
