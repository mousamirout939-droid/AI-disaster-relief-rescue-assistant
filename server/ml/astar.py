"""A* pathfinding, using haversine distance as the heuristic for lat/lng-tuple nodes."""
import heapq
from typing import Callable, Hashable, List, Tuple

from ml.graph_algorithms import Graph
from utils.location import haversine_km


def _default_heuristic(a: Hashable, b: Hashable) -> float:
    """Assumes nodes are (lat, lng) tuples; falls back to 0 (i.e. plain Dijkstra) otherwise."""
    if isinstance(a, tuple) and isinstance(b, tuple) and len(a) == 2 and len(b) == 2:
        return haversine_km(a[0], a[1], b[0], b[1])
    return 0.0


def astar(
    graph: Graph, start: Hashable, goal: Hashable,
    heuristic: Callable[[Hashable, Hashable], float] = _default_heuristic,
) -> Tuple[List[Hashable], float]:
    open_set = [(0.0, start)]
    g_score = {start: 0.0}
    previous: dict = {}
    visited = set()

    while open_set:
        _, node = heapq.heappop(open_set)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            path = [goal]
            while path[-1] != start:
                path.append(previous[path[-1]])
            path.reverse()
            return path, g_score[goal]

        for neighbor, weight in graph.neighbors(node):
            tentative_g = g_score[node] + weight
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                previous[neighbor] = node
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return [], float("inf")
