"""Dijkstra's shortest-path algorithm over a `ml.graph_algorithms.Graph`."""
import heapq
from typing import Hashable, List, Tuple

from ml.graph_algorithms import Graph


def dijkstra(graph: Graph, start: Hashable, goal: Hashable) -> Tuple[List[Hashable], float]:
    """Returns (path, total_distance). Path is empty if unreachable."""
    distances = {start: 0.0}
    previous: dict = {}
    visited = set()
    queue = [(0.0, start)]

    while queue:
        dist, node = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            break

        for neighbor, weight in graph.neighbors(node):
            new_dist = dist + weight
            if new_dist < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_dist
                previous[neighbor] = node
                heapq.heappush(queue, (new_dist, neighbor))

    if goal not in distances:
        return [], float("inf")

    path = [goal]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return path, distances[goal]
